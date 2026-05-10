from flask_migrate import Migrate
from blog.tools import db
from blog import create_app

"""
    code:
        40102 用户不存在、密码错误
"""

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
