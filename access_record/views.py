from flask import request, Blueprint
from.service import validate_password
from app import app

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def user_index():
    return 'User Index'

@user_bp.route('profile/<username>')
def user_profile(username):
    return f'User Profile: {username}'

@user_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return validate_password(username, password)