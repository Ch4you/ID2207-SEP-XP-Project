import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    # 加载环境变量 (来自 .env 和 .flaskenv)
    load_dotenv()

    app = Flask(__name__)
    
    # 从环境变量加载配置
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-secret-key',
        DEBUG=os.environ.get('FLASK_DEBUG') == '1'
    )

    # 注册路由蓝图 (Blueprints)
    from . import auth
    app.register_blueprint(auth.bp)

    from . import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/', endpoint='index')

    return app