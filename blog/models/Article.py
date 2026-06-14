# encoding:utf-8
from ..config import db
from .BaseModel import BaseModel

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
            "draft": self.draft,
            'createTime': self.createTime.strftime('%Y-%m-%d'),
            'category': self.category,
            'type': 'article'
        }

    def to_home_dict(self):
        return super().to_dict()