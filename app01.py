import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from access_record.views import access_record

app = Flask(__name__)

app.config.from_pyfile('config.py')

db.init_app(app)

app.register_blueprint(access_record)

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)