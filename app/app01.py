import sys
import os

# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db, User
from access_record.views import access_record
from config import config
from logging_config import setup_logging
setup_logging()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-for-testing-onlys'

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1小时
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400 * 7  # 7天
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(access_record, url_prefix='/api/v1')

if env == 'production' and not app.config.get('SECRET_KEY'):
    raise RuntimeError('生产环境错误: SECRET_KEY 环境变量未设置')

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/test')
def test():
    return jsonify({'message': 'Server is working'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("\n=== All registered routes ===")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.methods} -> {rule}")
    app.run(debug=app.config.get('DEBUG', False)) 