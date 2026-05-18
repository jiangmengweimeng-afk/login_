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

def generate_token(user_id):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    return access_token, refresh_token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if not auth_header:
                return jsonify({'message': 'Authorization 不存在'}), 401
            parts = auth_header.split()
            if len(parts) != 2 or parts[0] != 'Bearer':
                return jsonify({'message': '认证头格式错误'}), 401
            token = parts[1]

        if not token:
            return jsonify({'message': '缺少令牌 请登录后访问'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({'message': '用户不存在'}), 401
            request.current_user = {
                "id": user.id,
                "username": user.username
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌过期 请重新登录'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '令牌无效 非法访问'}), 401
        return f(*args, **kwargs)
    return decorated