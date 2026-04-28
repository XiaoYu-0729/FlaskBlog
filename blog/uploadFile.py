# encoding:utf-8
from datetime import datetime
from flask import Blueprint, request, jsonify
from blog.tools.tool import allowed_file, image_path, get_project_file
from blog.tools.module import Article, Project
from blog.tools.connect import db
import os
import uuid

upload = Blueprint('upload', __name__, url_prefix='/upload')

"""
    创建文章页面的封面上传来源：article
    创建项目页面的封面上传来源：project
    Markdown编辑器的图片上传来源：markdown
"""
# 图片下载到本地
@upload.route('/image', methods=['POST'])
def upload_image():
    try:
        source = request.form['source']
        original_image = request.files['file']  # 获取上传的文件(FileStorage对象,单个文件获取形式)
        image_name = original_image.filename    # 获取文件名
        # 路径处理
        image_type = os.path.splitext(image_name)[1]   # 获取图片扩展名
        unique_image = f'{uuid.uuid4().hex}{image_type}'   # 使用uuid生成唯一文件名
        base_path = image_path(source)
        unique_path = os.path.join(base_path, unique_image)
        # 上传文件到本地
        image_data = original_image.read()
        with open(unique_path, 'wb') as f:
            f.write(image_data)
        url = f'/send/image/{source}/{unique_image}'
        print(f'图片上传成功，返回数据为：{url}')
        return jsonify(url), 200
    except Exception as e:
        return jsonify(str(e)), 400

# 文件下载到本地
@upload.route('/files', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    path = 'D:\\BlogFiles\\files'
    try:
        if not allowed_file(files):
            raise Exception('Invalid file')
        results = []
        # 循环处理文件
        for file in files:
            # 生成安全文件
            file_type = file.filename.rsplit('.', 1)[1].lower()
            unique_file = f'{uuid.uuid4().hex}.{file_type}'
            file.save(os.path.join(path, unique_file))
            # 返回文件URL
            result = {'file_name': file.filename, 'uuid_name': unique_file}
            results.append(result)
    except Exception as e:
        return jsonify(str(e)), 400
    return jsonify(results), 200

# 文章上传数据库（待处理：Markdown长度格式验证）
@upload.route('/article', methods=['POST'])
def upload_article():
    article_data = request.get_json()
    # 转换时间格式(前端传递的是 ISO 8601 格式：2026-04-01T14:14:20.442Z)
    article_data['createTime'] = datetime.fromisoformat(article_data['createTime'].replace('Z', '+00:00'))
    print(f"文章数据：{article_data}")
    try:
        article = Article(**article_data)
        db.session.add(article)
        db.session.commit()
        print(f"文章提交成功。")
        return 'success', 200
    except Exception as e:
        db.session.rollback()
        print(f"数据库操作失败：{e}")
        return jsonify(str(e)), 400

# 项目上传数据库（待处理：Markdown长度格式验证）
@upload.route('/project', methods=['POST'])
def upload_project():
    project_data = request.get_json()
    files = project_data.pop('files')
    # 转换时间格式(前端传递的是 ISO 8601 格式：2026-04-01T14:14:20.442Z)
    project_data['createTime'] = datetime.fromisoformat(project_data['createTime'].replace('Z', '+00:00'))
    if project_data['startDate'] == '':
        project_data['startDate'] = None
    if project_data['endDate'] == '':
        project_data['endDate'] = None
    print(f"项目数据：{project_data}")
    try:
        # 录入项目表
        project = Project(**project_data)
        db.session.add(project)
        db.session.flush()    # 获取自动生成项目ID，但不提交
        files = get_project_file(files, project.id)
        print(f"项目id：{project}")
        # 录入项目文件表
        db.session.add_all(files)
        db.session.commit()
        print(f"项目提交成功")
        return 'success', 200
    except Exception as e:
        db.session.rollback()
        print(f"数据库操作失败：{e}")
        return  jsonify(str(e)), 400