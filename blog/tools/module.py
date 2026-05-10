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
    # 基础信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)                         # 头像文件名
    bio = db.Column(db.Text, nullable=True)                                   # 个人简介
    createTime = db.Column(db.DateTime, nullable=False)
    updateTime = db.Column(db.DateTime, nullable=False)
    # 统计
    articleCount = db.Column(db.Integer, nullable=False, default=0)
    projectCount = db.Column(db.Integer, nullable=False, default=0)
    visitorCount = db.Column(db.Integer, nullable=False, default=0)
    # commentCount = db.Column(db.Integer, nullable=False, default=0)
    # likeCount = db.Column(db.Integer, nullable=False, default=0)
    # collectCount = db.Column(db.Integer, nullable=False, default=0)
    # 权限
    status = db.Column(db.Integer, nullable=False, default=1)                  # 状态(0-禁用,1-正常)
    role = db.Column(db.String(20), nullable=False, default='user')
    lastLoginTime = db.Column(db.DateTime, nullable=True)
    lastLoginIp = db.Column(db.String(50), nullable=True)
    # 设置
    theme = db.Column(db.String(20), nullable=False, default='default')
    # 关系
    articles = db.relationship('Article', backref='user')
    projects = db.relationship('Project', backref='user')
    # 转换为字典
    def to_dict_detail(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'password': self.password,
            'email': self.email if self.email else None,
            'phone': self.phone if self.phone else None,
            'avatar': self.avatar if self.avatar else None,
            'bio': self.bio if self.bio else None,
            'createTime': self.createTime.strftime('%Y-%m-%d'),
            'updateTime': self.updateTime.strftime('%Y-%m-%d'),
            'articleCount': self.articleCount,
            'projectCount': self.projectCount,
            'visitorCount': self.visitorCount,
            'status': self.status,
            'role': self.role,
            'lastLoginTime': self.lastLoginTime.strftime('%Y-%m-%d') if self.lastLoginTime else None,
            'lastLoginIp': self.lastLoginIp if self.lastLoginIp else None,
            'theme': self.theme,
            'articles': [article.to_dict() for article in self.articles],
            'projects': [project.to_dict() for project in self.projects]
        }
    def to_dict(self):
        return {
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar if self.avatar else None
        }