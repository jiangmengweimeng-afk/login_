import jwt
from flask import Flask, request, jsonify, current_app
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None
        if auth_header and auth_required.stratswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'], 
                algorithms=['HS256'],
                options={'verify_exp': True}
            )
            current_user_id = payload.get('user_id')
            kwargs['user_id'] = current_user_id

        except jwt.ExpiredSginatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/profile')
@auth_required
def profile(user_id):
    return jsonify({'message': f'Welcome user{user_id}'}), 200