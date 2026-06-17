# encoding:utf-8
from ..config import db
from ..tools import ServerException
from ..models import Article, Project, User
from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies
from werkzeug.security import check_password_hash,generate_password_hash

ALLOWS_TYPE = ['article', 'project']

# 更新用户数据服务层
def update_user(data):
    try:
        response = jsonify({'message': 'success'})
        # 检查是否存在密码
        if 'newPassword' in data and 'currentPassword' in data:
            # 新密码不能与旧密码相同
            if data['newPassword'] == data['currentPassword']:
                raise ServerException('新密码不能与旧密码相同', 400)
            # 检查密码是否正确
            old_password = db.session.query(User).with_entities(User.password).filter(
                User.username == data['username']).first()
            if check_password_hash(old_password[0], data.pop('currentPassword')):
                new_password = data.pop('newPassword')
                data['password'] = generate_password_hash(new_password)
                unset_jwt_cookies(response)
            else:
                raise ServerException('旧密码错误', 400)
        username = data.pop('username')
        db.session.query(User).filter(User.username == username).update(data)
        db.session.commit()
        return response
    except Exception as e:
        db.session.rollback()
        raise e

# 检查点赞类型及该id下类型是否存在数据(文章/项目)
def check_like_type(id, username):
    user_id = db.session.query(User).with_entities(User.id).filter(User.username == username).first()
    # 处理合并类型的id
    id_type = id.split('-')[0]
    id = int(id.split('-')[1])
    if id_type not in ALLOWS_TYPE:
        raise ServerException('不支持的类型', 400)
    if id_type == 'project':
        target = Project.query.get(id)
    else:
        target = Article.query.get(id)
    if not target:
        raise ServerException(f'该{id_type}不存在', 404)
    return id, id_type, user_id[0]

# 点赞服务层
def add_like(id, username):
    try:
        id, id_type, user_id = check_like_type(id, username)
        # 点赞需要使用原生SQL处理
        sql_like = db.text("INSERT INTO `LIKE`(user_id, target_type, target_id, status, create_time) VALUES(:user_id, :target_type, :target_id, 1, NOW()) ON DUPLICATE KEY UPDATE status = 1, create_time = NOW()")
        result = db.session.execute(sql_like, {'user_id': user_id, 'target_type': id_type, 'target_id': id})
        if result and result.rowcount > 0:
            sql = db.text(f"UPDATE {id_type} SET like_count = like_count + 1 WHERE id = :id")
            db.session.execute(sql, {'id': id})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

# 取消点赞服务层
def cancel_like(id, username):
    try:
        id, id_type, user_id = check_like_type(id, username)
        sql_like = db.text("UPDATE `LIKE` SET status = 0 WHERE user_id = :user_id AND target_type = :target_type AND target_id = :target_id")
        result = db.session.execute(sql_like, {'user_id': user_id, 'target_type': id_type, 'target_id': id})
        if result and result.rowcount > 0:
            sql = db.text(f"UPDATE {id_type} SET like_count = like_count - 1 WHERE id = :id")
            db.session.execute(sql, {'id': id})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

# 收藏服务层
def add_collect(id, username):
    try:
        id, id_type, user_id = check_like_type(id, username)
        sql_collect = db.text("INSERT INTO COLLECT(user_id, target_type, target_id, status, create_time) VALUES(:user_id, :target_type, :target_id, 1, NOW()) ON DUPLICATE KEY UPDATE status = 1, create_time = NOW()")
        result = db.session.execute(sql_collect, {'user_id': user_id, 'target_type': id_type, 'target_id': id})
        if result and result.rowcount > 0:
            sql = db.text(f"UPDATE {id_type} SET collect_count = collect_count + 1 WHERE id = :id")
            db.session.execute(sql, {'id': id})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

# 取消收藏服务层
def cancel_collect(id, username):
    try:
        id, id_type, user_id = check_like_type(id, username)
        sql_collect = db.text("UPDATE COLLECT SET status = 0 WHERE user_id = :user_id AND target_type = :target_type AND target_id = :target_id")
        result = db.session.execute(sql_collect, {'user_id': user_id, 'target_type': id_type, 'target_id': id})
        if result and result.rowcount > 0:
            sql = db.text(f"UPDATE {id_type} SET collect_count = collect_count - 1 WHERE id = :id")
            db.session.execute(sql, {'id': id})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
