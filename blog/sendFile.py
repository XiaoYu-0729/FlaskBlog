# encoding:utf-8
from flask import Blueprint, send_from_directory, jsonify
from .tools import data_tool

send = Blueprint('send', __name__, url_prefix='/send')

# 使用GET请求可以让浏览器浏览图片，前端富文本编辑器才能正确识别
@send.route('/image/<source>/<image_name>',methods=['GET'])
def send_image(source, image_name):
    try:
        path = data_tool.image_path(source)
        return send_from_directory(path,image_name), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500