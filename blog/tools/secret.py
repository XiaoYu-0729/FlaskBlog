# encoding:utf-8
import base64
import secrets

# base64转换前格式检查
def check_base64(data):
    i = len(data) % 4
    if i:
        data += '=' * (4 - i)
    return data

# 随机生成JWT密钥
def get_jwt_secret_key():
    # 随机生成32字节
    random_bytes = check_base64(secrets.token_bytes(32))
    # 将字节转换为 base64 编码
    secret_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return secret_key