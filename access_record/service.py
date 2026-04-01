from flask import jsonify, request


def validate_password(username, password):
    if username == 'admin' and password == 'password':
        return jsonify({'code': 200, 'message': 'Login successful', 'data': {'username': 'admin'}})
    else:
        return jsonify({'code': 400, 'message': 'login failed or password failed'})