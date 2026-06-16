# encoding:utf-8

from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .config import db
from datetime import datetime, timezone
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, get_jwt_identity, create_refresh_token, set_refresh_cookies
from flasgger import swag_from

login = Blueprint('login', __name__, url_prefix='/login')

# 登录接口
@login.route('', methods=['POST'])
def get_login_info():
    try:
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        # 获取数据库查询结果
        user = User.query.filter_by(username=username).first()
        # 用户不存在检查
        if not user:
            return jsonify({'message': '用户不存在'}), 400
        # 用户被禁用检查
        if user.status == 0:
            return jsonify({'message': '该用户被禁用'}), 403
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
            return response, 200
        else:
            return jsonify({'message': '密码错误'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 注册接口
@login.route('/register', methods=['POST'])
@swag_from('api_docs/register.yml')
def register():
    # 数据处理
    data = request.get_json()
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

# 登出接口
@login.route('/logout', methods=['POST'])
def logout():
    try:
        response = jsonify({'message': 'success'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@login.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({'message': 'success'})
    set_access_cookies(response, access_token)
    return response, 200