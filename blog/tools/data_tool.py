# encoding:utf-8
from ..models import ProjectFile
from . import ServerException

ALLOWED_FILE = [
        'zip', 'rar', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'txt', 'rtf', 'xls', 'xlsx',
        'html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'properties', 'yml', 'yaml', 'c',
        'h', 'hpp'
    ]

"""
    创建文章页面的封面上传来源：article
    创建项目页面的封面上传来源：project
    Markdown编辑器的图片上传来源：markdown
    用户头像上传来源:avatar
"""
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
        raise ServerException('不支持的来源', 404)

# 判断文件名是否合法
def allowed_file(files):
    # 判断文件是否存在
    if not files:
        raise ServerException('文件不存在', 404)
    # 判断文件名是否合法
    for file in files:
        filename = file.filename
        if not filename or '.' not in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_FILE:
            raise ServerException('文件格式错误', 400)
    return

# 批量获取项目文件对象
def get_project_file(files_data, project_id):
    filelist = []
    for file in files_data:
        file_name = file['file_name']
        uuid_name = file['uuid_name']
        project_file = ProjectFile(fileName=file_name, uuidName=uuid_name, project_id=project_id)
        filelist.append(project_file)
    return filelist
