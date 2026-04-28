# encoding:utf-8
from flask import Flask
import blog.uploadFile
import blog.agent
import blog.sendFile
import blog.dataTransfer
from .tools import ConfigDB, db, Project, Article, ProjectFile

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigDB)
    # 初始化实例（配置）
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(uploadFile.upload)
    app.register_blueprint(agent.agent)
    app.register_blueprint(sendFile.send)
    app.register_blueprint(dataTransfer.data)
    # 若数据表不存在则创建数据表
    with app.app_context():
        db.create_all()
    return app