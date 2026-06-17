# encoding:utf-8
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, set_access_cookies
from ..models import User
from ..tools import ServerException
from ..config import db
from datetime import datetime, timezone

# 登录服务层
def get_login_info(data):
    username = data.get('username', None)
    password = data.get('password', None)
    # 获取数据库查询结果
    user = User.query.filter_by(username=username).first()
    # 用户不存在检查
    if not user: raise ServerException('用户不存在', 400)
    # 用户被禁用检查
    if user.status == 0: raise ServerException('该用户被禁用', 403)
    # 密码检查
    if check_password_hash(user.password, password):
        # 更新最后登录时间
        # db.session.query(User).filter(User.username == username).update({'lastLoginTime': datetime.now(timezone.utc)})
        # 签发token认证
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        response = jsonify({'message': 'success', 'userInfo': user.to_dict_base_data()})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    else:
        raise ServerException('密码错误', 400)

# 注册服务层
def register(data):
    try:
        nickname = f'用户{data["username"]}'
        createTime = datetime.now(timezone.utc)
        data['nickname'] = nickname  # data.update(nickname=nickname)
        data['createTime'] = createTime
        data['updateTime'] = createTime
        data['password'] = generate_password_hash(data['password'])
        print(f'注册用户：{data}')
        # 数据库操作
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        # 返回响应
        return jsonify({'message': 'success'})
    except Exception as e:
        db.session.rollback()
        raise e