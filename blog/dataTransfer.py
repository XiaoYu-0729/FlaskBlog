# encoding:utf-8
from flask import Blueprint, jsonify, request
from .models import  Article, Project, User, Like
from flask_jwt_extended import jwt_required,get_jwt_identity
from .tools import ServerException
from .server import DataTransferServer

data = Blueprint('data', __name__, url_prefix='/data')

# 获取首页全部数据
@data.route('/home', methods=['GET'])
def get_home_data():
    try:
        # 查询数据
        articles = Article.query.filter_by(draft=False)
        projects = Project.query.filter_by(draft=False)
        # 字典化
        articles = [article.to_home_dict() for article in articles]
        projects = [project.to_home_dict() for project in projects]
        print(f"文章数据：{articles}\n项目数据：{projects}")
        return jsonify({'articles': articles, 'projects': projects}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 获取文章/项目详情数据(路由已简化)
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

# 获取用户数据
@data.route('/user', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        username = get_jwt_identity()
        user_info = User.query.filter_by(username=username).first()
        if user_info.status == 0:
            return jsonify({'message': '该用户被禁用'}), 403
        return jsonify({'message': 'success', 'userInfo': user_info.to_dict_base_data()}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@data.route('/my-items', methods=['POST'])
@jwt_required()
def get_my_items():
    try:
        data = request.get_json()
        user_id = data['userId']
        type = data['type']
        if type == 'article':
            articles = Article.query.filter_by(user_id=user_id)
            data_list = [article.to_home_dict() for article in articles]
            return jsonify({'message': 'success', 'items': data_list}), 200
        elif type == 'project':
            projects = Project.query.filter_by(user_id=user_id)
            data_list = [project.to_home_dict() for project in projects]
            return jsonify({'message': 'success', 'items': data_list}), 200
        else:
            return jsonify({'message': 'type错误，无法识别是获取我的文章还是项目'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500