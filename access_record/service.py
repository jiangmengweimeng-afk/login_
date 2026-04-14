from flask import jsonify
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash


def validate_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return {
            'success': True,
            'user': {'username': user.username},
            'message': 'Login successful'
        }
    else:
        return {
            'success': False,
            'user': None,
            'message': 'Invalid username or password'
        }

def register_user(username, password):
    if User.query.filter_by(username=username).first():
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
        return {
            'success': True,
            'user': {'username': new_user.username},
            'message': 'User registered successfully'
        }
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'user': None,
            'message': f'Registration failed, please try again'
        }