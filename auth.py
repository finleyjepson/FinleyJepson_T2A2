from flask import request, jsonify, session, Blueprint
import os
import hashlib
from . import db
from .models import USER
import binascii
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token
from datetime import timedelta

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    # Check if username and password were provided
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if the username already exists in the database
    existing_user = USER.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Generate a random salt
    salt = os.urandom(16)
    salt_hex = binascii.hexlify(salt).decode()  # Convert salt to hexadecimal string

    # Hash the password with the salt
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hashed_password = binascii.hexlify(hashed_password).decode()

    # Create a new user
    new_user = USER(username=username, password=hashed_password, salt=salt_hex)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200

@auth.route('/login', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = USER.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    salt = binascii.unhexlify(user.salt.encode('utf-8'))  # Convert salt back to bytes

    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hashed_password = binascii.hexlify(hashed_password).decode()

    if hashed_password == user.password:
        expiry = timedelta(days=1)
        access_token = create_access_token(identity=str(user.userid), expires_delta=expiry)
        refresh_token = create_refresh_token(identity=str(user.userid), expires_delta=expiry)
        return jsonify({"message": "Logged In", "user": user.username, "tokens":{"access_token": access_token, "refresh_token": refresh_token}}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200