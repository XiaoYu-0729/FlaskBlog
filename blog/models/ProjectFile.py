# encoding:utf-8
from ..config import db

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