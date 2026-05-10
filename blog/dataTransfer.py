# encoding:utf-8
from flask import Blueprint, jsonify
from .tools import  Article, Project
from .tools.tool import get_home_dict

data = Blueprint('data', __name__, url_prefix='/data')

@data.route('/home', methods=['GET'])
def get_home_data():
    try:
        # 查询数据
        articles = Article.query.with_entities(Article.id,
            Article.title, Article.intro, Article.createTime)
        projects = Project.query.with_entities(Project.id,
            Project.title, Project.intro, Project.createTime)
        # 字典化
        articles = get_home_dict(articles)
        projects = get_home_dict(projects)
        print(f"文章数据：{articles}\n项目数据：{projects}")
        return jsonify({'articles': articles, 'projects': projects}), 200
    except Exception as e:
        return jsonify({'message': e}), 500

@data.route('/detail/<data_id>', methods=['GET'])
def get_detail_data(data_id):
    data_list = [item.strip() for item in data_id.split('-')]
    print(f"数据列表：{data_list}")
    try:
        if data_list[0] == 'article':
            article_id = int(data_list[1])
            article = Article.query.filter_by(id=article_id).first()
            print(f"文章数据：{article.to_dict()}")
            return jsonify(article.to_dict()), 200
        elif data_list[0] == 'project':
            project_id = int(data_list[1])
            project = Project.query.filter_by(id=project_id).first()
            print(f"项目数据：{project.to_dict()}")
            return jsonify(project.to_dict()), 200
        else:
            return jsonify({'message': 'id错误，无法识别是是什么类型的详情页'}), 400
    except Exception as e:
        return jsonify({'message': e}), 500