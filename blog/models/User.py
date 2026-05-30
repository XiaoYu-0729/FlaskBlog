# encoding:utf-8
from ..config import db

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