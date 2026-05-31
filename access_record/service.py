from flask import jsonify, request
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import jwt
import logging
import os
logger = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY', 'dev-secret-key-for-testing'))

def validate_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        logger.info(f'验证成功 - 用户：{username}')
        return {
            'success': True,
            'user': {'username': user.username, 'id': user.id},
            'message': 'Login successful'
        }
    else:
        logger.debug(f'登录验证 - 密码错误: {username}')
        return {
            'success': False,
            'user': None,
            'message': 'Invalid username or password'
        }

def register_user(username, password):
    if User.query.filter_by(username=username).first():
        logger.warning(f'注册失败 - 用户名已存在: {username}')
        return {
            'success': False,
            'user': None,
            'message': 'Username already exists'
        }

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        logger.debug(f'注册验证 - 用户创建成功: {username}')
        return {
            'success': True,
            'user': {'username': new_user.username},
            'message': 'User registered successfully'
        }
    except Exception as e:
        db.session.rollback()
        logger.exception(f'注册失败 - 数据库异常: {username}')
        return {
            'success': False,
            'user': None,
            'message': f'Registration failed, please try again'
        }