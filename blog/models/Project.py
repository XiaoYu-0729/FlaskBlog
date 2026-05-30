# encoding:utf-8
from .BaseModel import BaseModel
from ..config import db
import re

# 项目表
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