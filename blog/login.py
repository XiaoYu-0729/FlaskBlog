# encoding:utf-8

from flask import Blueprint,jsonify,request
from .server import LoginServer
from .tools import ServerException
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, get_jwt_identity
from flasgger import swag_from

login = Blueprint('login', __name__, url_prefix='/login')

# 登录路由(已简化)
@login.route('', methods=['POST'])
def get_login_info():
    try:
        data = request.get_json()
        result = LoginServer.get_login_info(data)
        return result, 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 注册路由(已简化)
@login.route('/register', methods=['POST'])
@swag_from('api_docs/register.yml')
def register():
    try:
        # 数据处理
        data = request.get_json()
        result = LoginServer.register(data)
        return result, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 登出路由
@login.route('/logout', methods=['POST'])
def logout():
    try:
        response = jsonify({'message': 'success'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 刷新token路由
@login.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({'message': 'success'})
    set_access_cookies(response, access_token)
    return response, 200