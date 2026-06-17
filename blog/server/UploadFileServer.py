# encoding:utf-8
from datetime import datetime
from ..config import db
from ..models import Project, Article
from ..tools import data_tool, ServerException
from flask import jsonify
import os,uuid

# 图片上传服务层
def upload_image(source, original_image):
    image_name = original_image.filename  # 获取文件名
    # 路径处理
    image_type = os.path.splitext(image_name)[1]  # 获取图片扩展名
    unique_image = f'{uuid.uuid4().hex}{image_type}'  # 使用uuid生成唯一文件名
    base_path = data_tool.image_path(source)
    unique_path = os.path.join(base_path, unique_image)
    # 上传文件到本地
    image_data = original_image.read()
    with open(unique_path, 'wb') as f:
        f.write(image_data)
    # 返回可直接被访问的图片URL
    url = f'/send/image/{source}/{unique_image}'
    print(f'图片上传成功，返回数据为：{url}')
    return jsonify(url)

# 文件上传服务层
def upload_files(files):
    path = 'D:\\BlogFiles\\files'
    data_tool.allowed_file(files)
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
    return jsonify(results)


# 创建文章服务层
def create_article(article_data):
    try:
        # 转换时间格式(前端传递的是 ISO 8601 格式：2026-04-01T14:14:20.442Z)
        article_data['createTime'] = datetime.fromisoformat(article_data['createTime'].replace('Z', '+00:00'))
        print(f"文章数据：{article_data}")
        article = Article(**article_data)
        db.session.add(article)
        # 更新用户文章数量
        sql = db.text("UPDATE USER SET articleCount = articleCount + 1 WHERE ID = :id")
        db.session.execute(sql, {'id': article_data['user_id']})
        db.session.commit()
        print(f"文章提交成功。")
        return jsonify({'message': 'success'})
    except Exception as e:
        db.session.rollback()
        print(f"数据库操作失败：{e}")
        raise e

# 创建项目服务层
def create_project(project_data, files):
    try:
        # 转换时间格式(前端传递的是 ISO 8601 格式：2026-04-01T14:14:20.442Z)
        project_data['createTime'] = datetime.fromisoformat(project_data['createTime'].replace('Z', '+00:00'))
        if project_data['startDate'] == '': project_data['startDate'] = None
        if project_data['endDate'] == '': project_data['endDate'] = None
        print(f"项目数据：{project_data}")
        # 录入项目表
        project = Project(**project_data)
        db.session.add(project)
        db.session.flush()  # 获取自动生成项目ID，但不提交
        files = data_tool.get_project_file(files, project.id)
        print(f"项目id：{project}")
        # 录入项目文件表
        db.session.add_all(files)
        # 更新用户项目数量
        sql = db.text("UPDATE USER SET projectCount = projectCount + 1 WHERE ID = :id")
        db.session.execute(sql, {'id': project_data['user_id']})
        db.session.commit()
        print(f"项目提交成功")
        return jsonify({'message': 'success'})
    except Exception as e:
        db.session.rollback()
        print(f"数据库操作失败：{e}")
        raise e