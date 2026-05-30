# encoding:utf-8
from flask import Blueprint, jsonify, request
from .models import  Article, Project, User
from .tools import data_tool, result_dict
from flask_jwt_extended import jwt_required,get_jwt_identity

data = Blueprint('data', __name__, url_prefix='/data')

# 获取首页全部数据
@data.route('/home', methods=['GET'])
def get_home_data():
    try:
        # 查询数据
        articles = Article.query.with_entities(Article.id, Article.draft, Article.view, Article.like,
            Article.title, Article.intro, Article.createTime, Article.coverName).filter_by(draft=False)
        projects = Project.query.with_entities(Project.id, Project.draft, Article.view, Article.like,
            Project.title, Project.intro, Project.createTime, Project.coverName).filter_by(draft=False)
        # 字典化
        articles = result_dict.get_home_dict(articles)
        projects = result_dict.get_home_dict(projects)
        print(f"文章数据：{articles}\n项目数据：{projects}")
        return jsonify({'articles': articles, 'projects': projects}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@data.route('/detail/<data_id>', methods=['GET'])
def get_detail_data(data_id):
    data_list = data_id.strip().split('-')
    print(f"数据列表：{data_list}")
    try:
        # 文章详情
        if data_list[0] == 'article':
            article_id = int(data_list[1])
            article = Article.query.filter_by(id=article_id, draft=False).first()
            if article is None:
                return jsonify({'message': '文章不存在'}), 404
            user = article.user
            print(f"文章数据：{article.to_dict()} 用户数据：{user.to_dict()}")
            return jsonify({
                'message': 'success',
                'data': article.to_dict(),
                'user': user.to_dict()
            }), 200
        # 项目详情
        elif data_list[0] == 'project':
            project_id = int(data_list[1])
            project = Project.query.filter_by(id=project_id, draft=False).first()
            if project is None:
                return jsonify({'message': '项目不存在'}), 404
            user = project.user
            print(f"项目数据：{project.to_dict()} 用户数据：{user.to_dict()}")
            return jsonify({
                'message': 'success',
                'data': project.to_dict(),
                'user': user.to_dict()
            }), 200
        # 错误
        else:
            return jsonify({'message': 'id错误，无法识别是是什么类型的详情页'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

"""
    .with_entities()方法和.first()方法结合返回命名元组对象，
    无法直接被JSON序列化(flask_sqlalchemy提供了._asdict()方
    法转化为字典，未来可能会发生改变)
"""
@data.route('/user', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        username = get_jwt_identity()
        user_info = User.query.with_entities(User.id, User.username,
                    User.nickname, User.avatar, User.bio, User.email, User.phone, User.articleCount,
                    User.visitorCount, User.projectCount, User.status,
                    User.role, User.theme).filter_by(username=username).first()
        if user_info.status == 0:
            return jsonify({'message': '该用户被禁用'}), 401
        return jsonify({'message': 'success', 'userInfo': user_info._asdict()}), 200
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
            articles = Article.query.with_entities(Article.id, Article.title, Article.view, Article.like,
                       Article.intro, Article.createTime, Article.coverName, Article.draft).filter_by(user_id=user_id)
            data_list = result_dict.get_home_dict(articles)
            return jsonify({'message': 'success', 'items': data_list}), 200
        elif type == 'project':
            projects = Project.query.with_entities(Project.id, Project.title, Project.view, Project.like,
                       Project.intro, Project.createTime, Project.coverName, Project.draft).filter_by(user_id=user_id)
            data_list = result_dict.get_home_dict(projects)
            return jsonify({'message': 'success', 'items': data_list}), 200
        else:
            return jsonify({'message': 'type错误，无法识别是获取我的文章还是项目'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500