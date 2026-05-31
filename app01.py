import sys
import os
from config import config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from access_record.views import access_record
from logging_config import setup_logging
setup_logging()

try:
    from access_record.views import access_record
    print("access_record blueprint imported successfully")
except Exception as e:
    print(f"Failed to import access_record: {e}")
    sys.exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-for-testing-onlyS'
# app.config.from_pyfile('config.py')

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])
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