# encoding:utf-8
from ..config import db

class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)            # 点赞的用户ID
    target_type = db.Column(db.String(20), nullable=False)                               # 点赞的目标类型(article,project)
    target_id = db.Column(db.Integer, nullable=False)                                    # 点赞的目标ID
    status = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref='likes')
    # 添加约束
    __table_args__ = (
        db.UniqueConstraint('user_id', 'target_type', 'target_id', name='unique_like_user_target'),
    )