# encoding:utf-8
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required
from .tools import db, User
from werkzeug.security import check_password_hash,generate_password_hash

update = Blueprint('update', __name__, url_prefix='/update')

@update.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        data = request.get_json()['data']
        # 检查是否存在密码
        if 'newPassword' in data and 'currentPassword' in data:
            # 新密码不能与旧密码相同
            if data['newPassword'] == data['currentPassword']:
                return jsonify({'message': '新密码不能与旧密码相同'}), 400
            # 检查密码是否正确
            old_password = db.session.query(User).with_entities(User.password).filter(User.username == data['username']).first()
            if check_password_hash(old_password[0], data.pop('currentPassword')):
                new_password = data.pop('newPassword')
                data['password'] = generate_password_hash(new_password)
            else:
                return jsonify({'message': '旧密码错误'}), 400
        username = data.pop('username')
        db.session.query(User).filter(User.username == username).update(data)
        db.session.commit()
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500