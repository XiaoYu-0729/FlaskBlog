# encoding:utf-8
from ..models import User, Like, Article, Project, Collect
from flask import jsonify
from ..tools import ServerException

# 获取首页数据服务层
def get_home_data():
    # 查询数据
    articles = Article.query.filter_by(draft=False)
    projects = Project.query.filter_by(draft=False)
    # 字典化
    articles = [article.to_home_dict() for article in articles]
    projects = [project.to_home_dict() for project in projects]
    print(f"文章数据：{articles}\n项目数据：{projects}")
    return jsonify({'articles': articles, 'projects': projects})

# 获取文章/项目详情数据服务层
def transfer_detail_data(data_id, username):
    data_list = data_id.strip().split('-')
    print(f"数据列表：{data_list}")
    # 检查登录状态
    is_login = False
    is_like = False
    is_collect = False
    if username:
        is_login = True
        user = User.query.filter_by(username=username).first()
        like = Like.query.filter_by(user_id=user.id, target_type=data_list[0], target_id=data_list[1]).first()
        collect = Collect.query.filter_by(user_id=user.id, target_type=data_list[0], target_id=data_list[1]).first()
        if like:  is_like = True
        if collect:  is_collect = True
    # 文章详情
    if data_list[0] == 'article':
        article_id = int(data_list[1])
        article = Article.query.filter_by(id=article_id, draft=False).first()
        if article is None:
            raise ServerException('文章不存在', 404)
        user = article.user
        print(f"文章数据：{article.to_dict()} 用户数据：{user.to_dict()}, 登录状态：{is_login}, 点赞状态：{is_like}")
        return jsonify({
            'message': 'success',
            'data': article.to_dict(),
            'user': user.to_dict(),
            'isLogin': is_login,
            'isLike': is_like,
            'isCollect': is_collect
        })
    # 项目详情
    elif data_list[0] == 'project':
        project_id = int(data_list[1])
        project = Project.query.filter_by(id=project_id, draft=False).first()
        if project is None:
            raise ServerException('项目不存在', 404)
        user = project.user
        print(f"项目数据：{project.to_dict()} 用户数据：{user.to_dict()}")
        return jsonify({
            'message': 'success',
            'data': project.to_dict(),
            'user': user.to_dict(),
            'isLogin': is_login,
            'isLike': is_like,
            'isCollect': is_collect
        })
    # 错误
    else:
        raise ServerException('id错误，无法识别是是什么类型的详情页', 400)

# 获取用户文章/项目服务层
def get_my_items(data):
    user_id = data['userId']
    type = data['type']
    if type == 'article':
        articles = Article.query.filter_by(user_id=user_id)
        data_list = [article.to_home_dict() for article in articles]
        return jsonify({'message': 'success', 'items': data_list})
    elif type == 'project':
        projects = Project.query.filter_by(user_id=user_id)
        data_list = [project.to_home_dict() for project in projects]
        return jsonify({'message': 'success', 'items': data_list})
    else:
        raise ServerException('type错误，无法识别是获取我的文章还是项目', 400)