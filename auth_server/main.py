import datetime
import hashlib
import json
import os

import jwt
from flask import Flask, jsonify, request
from methods import load_db, save_db

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')
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
        return jsonify({'message': 'Invalid credentials', 'success': False}), 401

    # As we store passwords in hashed form, we need to hash the password before comparing
    password = hashlib.md5(password.encode()).hexdigest()

    user = DB['users'].get(username)
    if user and DB['users'][username] == password:
        # Generate an access token and save it in the database
        payload = {
            'sub': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        user['token'] = access_token
        DB['users'][username] = user

        save_db(DB)
        return jsonify({'access_token': access_token, 'success': True})
    else:
        return jsonify({'message': 'Invalid credentials', 'success': False}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
