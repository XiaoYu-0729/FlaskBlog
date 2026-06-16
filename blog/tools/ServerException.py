# encoding:utf-8

# 自定义异常，处理服务内的业务异常
class ServerException(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code