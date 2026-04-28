# encoding:utf-8
import re

from sqlalchemy.orm import validates
from .connect import db

# 文章、项目基表（抽象类）
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)              # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 用户ID
    title = db.Column(db.String(255), nullable=False)         # 标题
    intro = db.Column(db.String(200), nullable=False)         # 简介
    content = db.Column(db.Text, nullable=False)              # 内容
    coverName = db.Column(db.String(255), nullable=True)      # 封面访问接口
    view = db.Column(db.Integer, nullable=False, default=0)   # 浏览量
    draft = db.Column(db.Boolean, nullable=False, default=False) # 是否为草稿
    createTime = db.Column(db.DateTime, nullable=False)       # 创建时间

    @validates('content')
    def validate_content(self, key, content):
        if len(content) > 100000:
            raise ValueError('Content is too long')
        return content

# 文章表
class Article(BaseModel):
    __tablename__ = 'article'
    category = db.Column(db.String(255), nullable=False)       # 文章分类
    # 转换为字典(基表新增：用户id,草稿)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'intro': self.intro,
            'content': self.content,
            'coverName': self.coverName,
            'view': self.view,
            'createTime': self.createTime.strftime('%Y-%m-%d'),
            'category': self.category,
            'type': 'article'
        }

# 项目表techStack
class Project(BaseModel):
    __tablename__ = 'project'
    techStack = db.Column(db.String(255), nullable=False)     # 技术栈
    status = db.Column(db.String(255), nullable=False)        # 项目状态
    startDate = db.Column(db.Date, nullable=True)             # 项目开始时间
    endDate = db.Column(db.Date, nullable=True)               # 项目结束时间
    files = db.relationship('ProjectFile', backref='project') # 项目文件(一对多)
    # 转换为字典(基表新增：用户id,草稿)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'coverName': self.coverName,
            'view': self.view,
            'createTime': self.createTime.strftime('%Y-%m-%d'),
            'intro': self.intro,
            'techStack': self.tech_stack_to_list(),
            'status': self.status,
            'startDate': self.startDate.strftime('%Y-%m-%d') if self.startDate else None,
            'endDate': self.endDate.strftime('%Y-%m-%d') if self.endDate else None,
            'files': [file.to_dict() for file in self.files],
            'type': 'project'
        }
    # 处理技术栈文本(转为列表)
    def tech_stack_to_list(self):
        if self.techStack:
            tech_stack_list = re.split('[,，]', self.techStack)
            return tech_stack_list
        else:
            return []

# 项目文件表
class ProjectFile(db.Model):
    __tablename__ = 'project_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)                                       # 主键
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)    # 项目ID
    uuidName = db.Column(db.String(255), nullable=False)                               # 文件UUID
    fileName = db.Column(db.String(255), nullable=False)                               # 文件名
    def to_dict(self):
        return {
            'id': self.id,
            'uuidName': self.uuidName,
            'fileName': self.fileName
        }

# 用户表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=True)
    profilePhoto = db.Column(db.String(255), nullable=True)
    # 文章(一对多)
    articles = db.relationship('Article', backref='user')
    # 项目(一对多)
    projects = db.relationship('Project', backref='user')