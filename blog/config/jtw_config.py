# encoding:utf-8
from ..tools import secret
import datetime

class JTWConfig():
    # 必须使用至少 32 字符的强密钥
    JWT_SECRET_KEY = 'flask-blog-super-secret-key-for-jwt-authentication-2026'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_CSRF_PROTECT = False  # 暂时关闭 CSRF 保护