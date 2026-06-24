# encoding:utf-8
import redis, logging
from flask import Flask
from . import uploadFile, agent,sendFile, dataTransfer, login, updateData
from .config import db, ConfigDB, ConfigSwagger, JTWConfig
from .tools import secret
from flask_jwt_extended import JWTManager
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    # 设置日志为调试级别状态
    app.logger.setLevel(logging.DEBUG)
    # 加载JTW配置
    app.config.from_object(JTWConfig)
    # 加载Swagger配置
    app.config.from_object(ConfigSwagger)
    # 配置Redis缓存(交给flask管理)
    app.config['REDIS_URL'] = 'redis://127.0.0.1:6379/0'
    app.redis = redis.Redis.from_url(
        app.config['REDIS_URL'],
        decode_responses=True,
        max_connections = 10
    )
    # 加载数据库配置
    app.config.from_object(ConfigDB)
    # 数据库实例与当前应用绑定
    db.init_app(app)
    # 初始化JWT
    JWTManager(app)
    # Swagger配置
    Swagger(app)
    # 注册蓝图
    app.register_blueprint(uploadFile.upload)
    app.register_blueprint(agent.agent)
    app.register_blueprint(sendFile.send)
    app.register_blueprint(dataTransfer.data)
    app.register_blueprint(login.login)
    app.register_blueprint(updateData.update)
    # 若数据表不存在则创建数据表
    with app.app_context():
        db.create_all()
    return app