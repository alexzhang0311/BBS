from flask import Flask
from flask_wtf import CSRFProtect
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from exts import db,mail
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app=app)
    mail.init_app(app=app)
    CSRFProtect(app=app)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    return app
#蓝图：前台、后台、公共
#文件结构：config.py/exts.py/models.py/manage.py/forms.py


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
