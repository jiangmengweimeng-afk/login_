from flask_jwt_extended import(
    create_access_token,
    create_refresh_toekn,
    refresh_jwt_required
)

@app.route("/login", methods=['POST'])
def login():
    username = request.get_json().get("username")
    password = request.get_json().get("password")

    if username == 'alice' and password == 'password123':
        access_token = create_access_token(identify=username)
        refresh_token = create_refresh_toekn(identify=username)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    return jsonify({'message': '登录失败'}), 401

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identify()
    new_access_token = create_access_token(identify=current_user)
    return jsonify({'access_token': new_access_token}), 200

@app.route('/protedted', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': f'欢迎{get_jwt_identify()}'}), 200