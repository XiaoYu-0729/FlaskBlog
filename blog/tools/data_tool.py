# encoding:utf-8
from openai import OpenAI
from ..models import ProjectFile

ALLOWED_FILE = [
        'zip', 'rar', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'txt', 'rtf', 'xls', 'xlsx',
        'html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'properties', 'yml', 'yaml', 'c',
        'h', 'hpp'
    ]

def image_path(source):
    if source == 'markdown':
        return 'D:\\BlogFiles\\images\\markdown'
    elif source == 'article':
        return 'D:\\BlogFiles\\images\\article'
    elif source == 'project':
        return 'D:\\BlogFiles\\images\\project'
    elif source == 'avatar':
        return 'D:\\BlogFiles\\images\\avatar'
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
