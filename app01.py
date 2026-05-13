import sys
import os
from config import config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from access_record.views import access_record
from logging_config import setup_logging
setup_logging()

app = Flask(__name__)

# app.config.from_pyfile('config.py')

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])
db.init_app(app)

app.register_blueprint(access_record)

if env == 'production' and not app.config.get('SECRET_KEY'):
    raise RuntimeError('生产环境错误: SECRET_KEY 环境变量未设置')

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)