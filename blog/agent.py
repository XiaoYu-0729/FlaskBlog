# encoding:utf-8

from flask import Blueprint,request,jsonify
from .tools import agent_response

agent = Blueprint('agent', __name__, url_prefix='/agent')

@agent.route('/message', methods=['POST'])
def agent_info():
    try:
        data = request.get_json()
        print(f"用户提问的数据：{data}")
        if data['type'] == 'general':
            sys_content = "你是有学识、耐心且诚实的助手。用清晰、有帮助的方式回应用户。"
        else:
            sys_content = "你是一个基于提供的数据回答问题的助手。只根据给出的数据库内容进行回答。如果内容里没有相关信息，请直接说“不知道”或“未找到”。回答要准确、简洁。"
        content = agent_response.get_agent_info(data['text'], sys_content)
        return jsonify(content), 200
    except Exception as e:
        str = f"服务器出现错误：{e}。请联系系统管理员。"
        return jsonify({'message': str}), 500