# encoding:utf-8
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .tools import ServerException
from .server import UpdateDataServer

update = Blueprint('update', __name__, url_prefix='/update')

# 更新用户信息路由(已简化)
@update.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        data = request.get_json()
        result = UpdateDataServer.update_user(data)
        return result, 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 点赞路由(已简化)
@update.route('/<string:id>/like', methods=['POST'])
@jwt_required()
def like(id):
    try:
        username = get_jwt_identity()
        UpdateDataServer.add_like(id, username)
        return jsonify({'message': 'success'}), 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 取消点赞路由(已简化)
@update.route('/<string:id>/like', methods=['DELETE'])
@jwt_required()
def cancel_like(id):
    try:
        username = get_jwt_identity()
        UpdateDataServer.cancel_like(id, username)
        return jsonify({'message': 'success'}), 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 收藏路由(已简化)
@update.route('/<string:id>/collect', methods=['POST'])
@jwt_required()
def collect(id):
    try:
        username = get_jwt_identity()
        UpdateDataServer.add_collect(id, username)
        return jsonify({'message': 'success'}), 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 取消收藏路由(已简化)
@update.route('/<string:id>/collect', methods=['DELETE'])
@jwt_required()
def cancel_collect(id):
    try:
        username = get_jwt_identity()
        UpdateDataServer.cancel_collect(id, username)
        return jsonify({'message': 'success'}), 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code