from flask import json
from flask import current_app as app
from ..models import Article, Project
from ..tools import ServerException

# 获取首页数据数据库层
def get_home_data():
    # 从Redis缓存中获取文章和项目数据
    redis_articles = app.redis.get('home:articles')
    redis_projects = app.redis.get('home:projects')
    # 文章命中判断
    if not redis_articles:
        articles = Article.query.filter_by(draft=False).all()
        articles = [article.to_home_dict() for article in articles]
        app.redis.setex('home:articles', 3600, json.dumps(articles))
    else:
        articles = json.loads(redis_articles)
    # 项目命中判断
    if not redis_projects:
        projects = Project.query.filter_by(draft=False).all()
        projects = [project.to_home_dict() for project in projects]
        app.redis.setex('home:projects', 3600, json.dumps(projects))
    else:
        projects = json.loads(redis_projects)
    app.logger.debug(f"文章数据：{articles}\n项目数据：{projects}")
    return {'articles': articles, 'projects': projects}

# 获取详情页数据数据库层
def get_detail_data(data_list):
    # 文章详情
    if data_list[0] == 'article':
        article_id = int(data_list[1])
        # Redis缓存查找文章详情
        redis_article = app.redis.get(f'detail:article:{article_id}')
        if not redis_article:
            article = Article.query.filter_by(id=article_id, draft=False).first()
            if article is None: raise ServerException('文章不存在', 404)
            user = article.user
            result = {'data':article.to_dict(), 'user': user.to_dict()}
            # 文章详情存入Redis
            app.redis.setex(f'detail:article:{article_id}', 3600, json.dumps(result))
            return result
        else:
            return json.loads(redis_article)
    # 项目详情
    elif data_list[0] == 'project':
        project_id = int(data_list[1])
        # Redis缓存查找项目详情
        redis_project = app.redis.get(f'detail:project:{project_id}')
        if not redis_project:
            project = Project.query.filter_by(id=project_id, draft=False).first()
            if project is None: raise ServerException('项目不存在', 404)
            user = project.user
            result = {'data': project.to_dict(), 'user': user.to_dict()}
            # 项目详情存入Redis
            app.redis.setex(f'detail:project:{project_id}', 3600, json.dumps(result))
            return result
        else:
            return json.loads(redis_project)
    # 错误
    else:
        raise ServerException('id错误，无法识别是是什么类型的详情页', 400)

# 获取用户文章/项目列表数据库层
def get_my_items(data):
    user_id = data['userId']
    if data['type'] == 'article':
        # Redis获取用户文章
        redis_articles = app.redis.get(f'my-items:articles:{user_id}')
        if not redis_articles:
            articles = Article.query.filter_by(user_id=user_id).all()
            data_list = [article.to_home_dict() for article in articles]
            # 用户文章存入Redis
            app.redis.setex(f'my-items:{user_id}:articles', 3600, json.dumps(data_list))
            return data_list
        else:
            return json.loads(redis_articles)
    elif data['type'] == 'project':
        # Redis获取用户项目
        redis_projects = app.redis.get(f'my-items:projects:{user_id}')
        if not redis_projects:
            projects = Project.query.filter_by(user_id=user_id).all()
            data_list = [project.to_home_dict() for project in projects]
            # 用户项目存入Redis
            app.redis.setex(f'my-items:{user_id}:projects', 3600, json.dumps(data_list))
            return data_list
        else:
            return json.loads(redis_projects)
    else:
        raise ServerException('type错误，无法识别是获取我的文章还是项目', 400)