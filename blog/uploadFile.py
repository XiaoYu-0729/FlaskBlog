# encoding:utf-8
from flask import Blueprint, request, jsonify
from .tools import ServerException
from .server import UploadFileServer
from flask_jwt_extended import jwt_required

upload = Blueprint('upload', __name__, url_prefix='/upload')

# 图片上传路由(已简化)
@upload.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    try:
        source = request.form['source']
        original_image = request.files['file']  # 获取上传的文件(FileStorage对象,单个文件获取形式)
        result = UploadFileServer.upload_image(source, original_image)
        return result, 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': e}), 500

# 文件上传(已简化)
@upload.route('/files', methods=['POST'])
@jwt_required()
def upload_files():
    try:
        files = request.files.getlist('files')
        result = UploadFileServer.upload_files(files)
        return result, 200
    except ServerException as e:
        return jsonify({'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 创建文章路由(已简化)
@upload.route('/article', methods=['POST'])
@jwt_required()
def upload_article():
    try:
        article_data = request.get_json()
        result = UploadFileServer.create_article(article_data)
        return result, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 创建项目路由(已简化)
@upload.route('/project', methods=['POST'])
@jwt_required()
def upload_project():
    try:
        project_data = request.get_json()
        files = project_data.pop('files')
        result = UploadFileServer.create_project(project_data, files)
        return result, 200
    except Exception as e:
        return  jsonify({'message': str(e)}), 500