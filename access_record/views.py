from flask import Blueprint, jsonify, request
from .service import validate_password, register_user


access_record = Blueprint('access_record', __name__, url_prefix='/access_record')

@access_record.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': 'no json data no provided'}), 400
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'code': 400,
            'message': 'username and password are required'
        }), 400
    
    result = validate_password(username, password)

    if result['success']:
        return jsonify({
            'code': 200,
            'message': 'login successful',
            'data': result['user']
        }), 200
    else:
        return jsonify({
            'code': 401,
            'message': result['message']
        }), 401

@access_record.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            'code': 400,
            'message': 'no json data no provided'
        }), 400
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        




    
    