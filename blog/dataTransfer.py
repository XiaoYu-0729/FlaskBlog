# encoding:utf-8
from flask import Blueprint, jsonify, request
from .models import User
from flask_jwt_extended import jwt_required,get_jwt_identity
from .tools import ServerException
from .server import DataTransferServer

data = Blueprint('data', __name__, url_prefix='/data')

# 获取首页数据路由(已简化)
@data.route('/home', methods=['GET'])
def get_home_data():
    try:
        result = DataTransferServer.get_home_data()
        return result, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 获取文章/项目详情数据路由(已简化)
@data.route('/detail/<data_id>', methods=['GET'])
@jwt_required(optional=True)
def get_detail_data(data_id):
    try:
        username = get_jwt_identity()
        response = DataTransferServer.transfer_detail_data(data_id, username)
        return response, 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 获取用户信息路由
@data.route('/user', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        username = get_jwt_identity()
        user_info = User.query.filter_by(username=username).first()
        if user_info.status == 0: raise ServerException('用户被禁用', 403)
        return jsonify({'message': 'success', 'userInfo': user_info.to_dict_base_data()}), 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 获取用户的文章/项目路由(已简化)
@data.route('/my-items', methods=['POST'])
@jwt_required()
def get_my_items():
    try:
        data = request.get_json()
        result = DataTransferServer.get_my_items(data)
        return result, 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500