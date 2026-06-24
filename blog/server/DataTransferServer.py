# encoding:utf-8
from ..models import User, Like, Collect
from flask import jsonify
from ..repository import DataTransferRepository
from flask import current_app as app

# 获取首页数据服务层(已简化)
def get_home_data():
    # 查询数据
    result = DataTransferRepository.get_home_data()
    return jsonify(result)

# 获取文章/项目详情数据服务层(已简化)
def get_detail_data(data_id, username):
    data_list = data_id.strip().split('-')
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
    result = DataTransferRepository.get_detail_data(data_list)
    result.update({'message': 'success', 'isLogin': is_login, 'isLike': is_like, 'isCollect': is_collect})
    app.logger.debug(f'详情数据：{result}')
    return jsonify(result)

# 获取用户文章/项目服务层(已简化)
def get_my_items(data):
    result = DataTransferRepository.get_my_items(data)
    return jsonify({'message': 'success', 'items': result})