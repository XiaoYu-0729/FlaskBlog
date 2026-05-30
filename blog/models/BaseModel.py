# encoding:utf-8
from sqlalchemy.orm.mapper import validates
from ..config import db

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
    like = db.Column(db.Integer, nullable=False, default=0)   # 点赞量
    draft = db.Column(db.Boolean, nullable=False, default=False) # 是否为草稿
    createTime = db.Column(db.DateTime, nullable=False)       # 创建时间

    @validates('content')
    def validate_content(self, key, content):
        if len(content) > 100000:
            raise ValueError('Content is too long')
        return content