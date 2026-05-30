# encoding:utf-8

# 处理数据库返回数据的字典化
def get_home_dict(data):
    result = [
        {
            'id': item.id,
            'title': item.title,
            'intro': item.intro,
            'createTime': item.createTime.strftime('%Y-%m-%d'),
            'coverName': item.coverName,
            "draft": item.draft,
            "view": item.view,
            "like": item.like
        }
        for item in data
    ]
    return result