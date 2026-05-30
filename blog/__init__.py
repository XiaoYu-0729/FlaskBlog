# encoding:utf-8
from flask import Flask
from . import uploadFile, agent,sendFile, dataTransfer, loginModel, updateData
from .config import db, ConfigDB, ConfigSwagger
from .tools import secret
from flask_jwt_extended import JWTManager
from flasgger import Swagger

import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigSwagger)
    # 加载数据库配置
    app.config.from_object(ConfigDB)
    # 数据库实例与当前应用绑定
    db.init_app(app)
    # JWT密钥和过期时间设置
    app.config['JWT_SECRET_KEY'] = secret.get_jwt_secret_key()
    app.config['JWT ACCESS TOKEN EXPIRES'] = datetime.timedelta(hours=1)
    # 初始化JWT
    JWTManager(app)
    # Swagger配置
    Swagger(app)
    # 注册蓝图
    app.register_blueprint(uploadFile.upload)
    app.register_blueprint(agent.agent)
    app.register_blueprint(sendFile.send)
    app.register_blueprint(dataTransfer.data)
    app.register_blueprint(loginModel.login)
    app.register_blueprint(updateData.update)
    # 若数据表不存在则创建数据表
    with app.app_context():
        db.create_all()
    return app