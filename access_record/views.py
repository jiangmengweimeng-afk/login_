from flask import Blueprint, jsonify, request, make_response
from .service import validate_password, register_user, generate_token
from common.auth import login_required, create_access_token, create_refresh_token
import logging
import jwt

logger = logging.getLogger(__name__)

access_record = Blueprint('access_record', __name__, url_prefix='/access_record')

@access_record.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400
    
    result = validate_password(username, password)
    if not result['success']:
        return jsonify({'code': 401, 'message': result['message']}), 401
    user = result['user']

    access_token = create_access_token(user['id'])
    refresh_token = create_refresh_token(user['id'])

    response = make_response(jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }))

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=7*24*60*60
    )
    return response

@access_record.route('/login', methods=['POST'])
def login():
    ip = request.remote_addr
    data = request.get_json()
    username = data.get('username') if data else None
    logger.info(f'收到登录请求 - IP: {ip} - 用户名: {username}')
   

    if not data:
        return jsonify({'code': 400, 'message': 'no json data no provided'}), 400
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning(f'参数验证失败 - IP: {ip} - 原因: 用户名或密码为空')
        return jsonify({
            'code': 400,
            'message': 'username and password are required'
        }), 400
    
    result = validate_password(username, password)
    

    if result['success']:
        logger.info(f'登录成功 - IP: {ip} - 用户名: {username}')
        token = generate_token(user_id=result['user']['id'], username=result['user']['username'])
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return jsonify({
            'code': 200,
            'message': 'login successful',
            'data': result['user'],
            'token': token,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        error_msg = result.get('message', '未知错误')
        logger.warning(f'登录失败 - IP:{ip} - 用户名: {username}, 原因: {error_msg}')
        return jsonify({
            'code': 401,
            'message': result['message']
        }), 401

@access_record.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': 'no json data no provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    logger.info(f'收到注册请求 - 用户名: {username}')

    if not username or not password:
        logger.warning(f'注册参数验证失败 - 用户名: {username} - 原因: 密码和用户名不能为空')
        return jsonify({'code': 400, 'message': 'Username and password cannot be empty'}), 400
    
    if  not username.strip() or not password.strip():
        return jsonify({'code': 400, 'message': 'Username and password cannot be empty string'}), 400
    
    if len(password) < 6:
        logger.warning(f'注册失败 - 用户名: {username} - 原因: 密码长度不足')
        return jsonify({'code': 400, 'message': '密码长度不符合要求'}), 400
    
    result = register_user(username, password)

    if result['success'] is True:
        logger.info(f'注册成功 - 用户名: {username}')
        return jsonify({'code': 201, 'message': 'Register successful', 'data': result['user']}), 201
    elif result['success'] is False:
        if 'already exists' in result['message'].lower():
            logger.warning(f'注册失败 - 用户名： {username} - 原因： 用户名已经存在')
            return jsonify({'code': 409, 'message': 'Username already exists'}), 409
        else:
            logger.warning(f'注册失败 - 用户名: {username} - 原因: 服务器内部错误')
            return jsonify({'code': 500, 'message': 'Internal server error'}), 500
    else:
        return jsonify({'code': 400, 'message': 'others reason'}), 400
    
@access_record.route('/profile', methods=['GET'])
@login_required
def profile():
    user = request.current_user
    return jsonify({
        'message': f'你好 欢迎 {user["username"]} 来到后台 dashboard',
        'user': user,
        'token': request.headers.get('Authorization')
        })

@access_record.route('/api/refresh', methods=['POST'])
def refresh_access_token():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token missing'}), 401
    
    try:
        payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload['sub']
        user_id = payload['user_id']
        new_access_token, new_refresh_token = generate_token(user_id, username)
        
        response = make_response(jsonify({
            'refresh_token': new_refresh_token,
            'access_token': new_access_token,
            'token_type': 'Bearer'
        }))

        response.set_cookie(
            key='refresh_token',
            value=new_refresh_token,
            httponly=True,
            sercure=True,
            samesite='Lax',
            max_age=7*24*60*60
        )
        return response
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token 已过期 请重新登录'}),401
    except jwt.InvalidTokenError:
        return jsonify({'message': '无效的 Refresh token'}), 401