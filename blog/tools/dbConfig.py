# encoding:utf-8

# 数据库配置
USERNAME = 'xiaoyu'
PASSWORD = 'XiaoYu0729'
HOST = 'localhost'
PORT = 3306
DATABASE = 'flaskblog'

class ConfigDB:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True    # 打印 SQL 语句（开发环境可设为 True，方便调试）
    # 引擎高级配置（如连接池大小、超时等）
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,  # 避免 MySQL 8小时空闲断开
        'pool_pre_ping': True,  # 自动重连检测
    }