import datetime
import hashlib
import os

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from methods import load_db, save_db_changes

load_dotenv('.auth-env')

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_VERIFICATION_HOST = os.getenv('ALLOWED_VERIFICATION_HOST')
ALLOWED_VERIFICATION_PORT = os.getenv('ALLOWED_VERIFICATION_PORT')

DB = load_db()


@app.route('/authorize', methods=['POST'])
def authorize():
    """
    This endpoint is used by the client to request an access token.
    Request body should contain username and password.
    If the credentials are valid, the endpoint returns an access token.
    """
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        print(f'Invalid credentials, failed to log in, 401')
        return jsonify({'message': 'Invalid credentials', 'success': False}), 401

    # As we store passwords in hashed form, we need to hash the password before comparing
    password = hashlib.md5(password.encode()).hexdigest()

    user = DB['users'].get(username)
    print(DB['users'])
    if user and DB['users'][username]['password'] == password:
        # Generate an access token and save it in the database
        payload = {
            'sub': username,
            'exp': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        user['token'] = access_token
        DB['users'][username] = user

        save_db_changes(DB)
        print(f'User {username} logged in successfully, 200')
        return jsonify({'access_token': access_token, 'success': True})
    else:
        print(f'Invalid credentials, failed to log in, 401')
        return jsonify({'message': 'Invalid credentials', 'success': False}), 401


@app.route('/verify_token', methods=['POST'])
def verify_token():
    """
    This endpoint is used by the Resource API to verify the validity of an access token.
    Request body should contain an access token.
    If the token is valid, it returns a success response; otherwise, it returns an error response.
    """
    # Check if the request is coming from the Resource API (localhost:5000)
    if request.remote_addr != ALLOWED_VERIFICATION_HOST \
            or request.environ['REMOTE_PORT'] != ALLOWED_VERIFICATION_PORT:
        print('Unauthorized, 401')
        return jsonify({'message': 'Unauthorized', 'valid': False}), 401

    data = request.get_json()
    access_token = data.get('access_token', None)

    if not access_token:
        print('Access token is missing')
        return jsonify({'message': 'Access token is missing', 'valid': False}), 400

    try:
        # Verify the access token's signature using the SECRET_KEY
        jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        print('Access token is valid, 200')
        return jsonify({'valid': True}), 200

    except jwt.ExpiredSignatureError:
        print('Access token has expired, 401')
        return jsonify({'message': 'Access token has expired', 'valid': False}), 401

    except jwt.DecodeError:
        print('Invalid access token, 401')
        return jsonify({'message': 'Invalid access token', 'valid': False}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
