# encoding:utf-8

from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .config import db
from datetime import datetime, timezone
from flask_jwt_extended import create_access_token
from flasgger import swag_from

login = Blueprint('login', __name__, url_prefix='/login')

# 登录接口
@login.route('', methods=['POST'])
def get_login_info():
    try:
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        # 获取数据库查询结果(返回命名元组对象)
        db_password = db.session.query(User).with_entities(User.password, User.status).filter(User.username == username).first()
        # 用户不存在检查
        if len(db_password) == 0:
            return jsonify({'message': '用户不存在'}), 401
        # 用户被禁用检查
        if db_password[1] == 0:
            return jsonify({'message': '该用户被禁用'}), 401
        # 密码检查
        if check_password_hash(db_password[0], password):
            # 签发token认证
            access_token = create_access_token(identity=username)
            # 更新最后登录时间
            # db.session.query(User).filter(User.username == username).update({'lastLoginTime': datetime.now(timezone.utc)})
            return jsonify({
                'message': 'success',
                'token': access_token,

            }), 200
        else:
            return jsonify({'message': '密码错误'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 注册接口
@login.route('/register', methods=['POST'])
@swag_from('api_docs/register.yml')
def register():
    # 数据处理
    data = request.get_json()
    del data['_skipAuth']
    nickname = f'用户{data["username"]}'
    createTime = datetime.now(timezone.utc)
    data['nickname'] = nickname     # data.update(nickname=nickname)
    data['createTime'] = createTime
    data['updateTime'] = createTime
    data['password'] = generate_password_hash(data['password'])
    print(f'注册用户：{data}')
    try:
        # 数据库操作
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        # 返回响应
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500