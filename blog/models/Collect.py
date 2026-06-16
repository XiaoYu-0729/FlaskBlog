# encoding:utf-8
from ..config import db

class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)       # 收藏的用户ID
    target_type = db.Column(db.String(20), nullable=False)                          # 收藏目标类型(article,project)
    target_id = db.Column(db.Integer, nullable=False)                               # 收藏的目标ID
    isUse = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref='collects')