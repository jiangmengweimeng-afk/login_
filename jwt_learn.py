from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

SECRET_KEY = 'my_super_sercet_key_12345'

def generate_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'role': 'admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': '缺少令牌， 请登录后再访问'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': ''})