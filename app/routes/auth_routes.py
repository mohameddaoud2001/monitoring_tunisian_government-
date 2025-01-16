from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db
from flask_smorest import Blueprint, abort
from app import limiter

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        role=data.get('role', 'citizen'),
        jurisdiction=data.get('jurisdiction')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
@limiter.limit("5/minute")
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'jurisdiction': user.jurisdiction}
    )
    return jsonify({'access_token': access_token}), 200

@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        abort(404, message="User not found")

    return jsonify({
        'message': 'This is a protected route',
        'user_id': current_user_id,
        'username': user.username,
        'role': user.role,
        'jurisdiction': user.jurisdiction
    }), 200
