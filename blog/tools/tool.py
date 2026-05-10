# encoding:utf-8
from openai import OpenAI
from blog.tools import ProjectFile
import secrets
import base64

ALLOWED_FILE = [
        'zip', 'rar', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'txt', 'rtf', 'xls', 'xlsx',
        'html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'properties', 'yml', 'yaml', 'c',
        'h', 'hpp'
    ]

BASE_URL = 'https://api.minimaxi.com/v1'
API_KEY = 'sk-cp-Ng7Lqc87wwJkFagZIWbAYe5VqZZ3S65Bsn42tX0vSrRm8y9j-VCBl7qOs7P9DVqArD7wieRfm6LzaW3VAbJDmGPFXpngIx0QdjhodINTJj6fuj1gboSbzk8'

def image_path(source):
    if source == 'markdown':
        return 'D:\\BlogFiles\\markdown'
    elif source == 'article':
        return 'D:\\BlogFiles\\article'
    elif source == 'project':
        return 'D:\\BlogFiles\\project'
    else:
        raise Exception('Invalid source')

# 判断文件名是否合法
def allowed_file(files):
    # 判断文件是否存在
    if not files:
        return False
    # 判断文件名是否合法
    for file in files:
        filename = file.filename
        if not filename or '.' not in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_FILE:
            return False
    return True

# 批量获取项目文件对象
def get_project_file(files_data, project_id):
    filelist = []
    for file in files_data:
        file_name = file['file_name']
        uuid_name = file['uuid_name']
        project_file = ProjectFile(fileName=file_name, uuidName=uuid_name, project_id=project_id)
        filelist.append(project_file)
    return filelist

# 处理数据库返回数据的字典化
def get_home_dict(data):
    result = [
        {
            'id': item.id,
            'title': item.title,
            'intro': item.intro,
            'createTime': item.createTime.strftime('%Y-%m-%d')
        }
        for item in data
    ]
    return result

# base64转换前格式检查
def check_base64(data):
    i = len(data) % 4
    if i:
        data += '=' * (4 - i)
    return data

# 随机生成JWT密钥
def get_jwt_secret_key():
    # 随机生成32字节
    random_bytes = check_base64(secrets.token_bytes(32))
    # 将字节转换为 base64 编码
    secret_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return secret_key

# 获取智能体回复
def get_agent_info(content, sys_content):
    # 创建 OpenAI 对象
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    # 创建 ChatCompletion 对象
    response = client.chat.completions.create(
        model='MiniMax-M2.7',
        messages=[  # type: ignore
            {"role": "system", "content": sys_content},
            {"role": "user", "content": content},
        ],
        # 设置 reasoning_split=True 将思考内容分离到 reasoning_details 字段
        extra_body={"reasoning_split": True},
    )
    text = response.choices[0].message.content
    # print(f"Thinking:\n{response.choices[0].message.reasoning_details[0]['text']}\n")
    print(f"智能体回复:\n{text}\n")
    return text

if __name__ == '__main__':
    get_agent_info("今天吃什么比较好？", "你是一个智能助手，请根据用户输入的内容给出一个回答。")