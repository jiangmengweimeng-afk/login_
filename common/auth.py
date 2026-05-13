from functools import wraps
from flask import request, jsonify, current_app
from models import RefreshToken, User, db
import jwt
import os
import datetime

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY'))

def create_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'type': 'access'
        }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def create_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'type': 'refresh'
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    rt = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.session.add(rt)
    db.session.commit()
    return token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[1]
        if not token:
            return jsonify({'message': '未登录 请登录后再访问'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌过期 请重新登录'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效令牌 非法访问'}), 401
        return f(*args, **kwargs)
    return decorated