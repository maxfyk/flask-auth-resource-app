import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv('.resource-env')

app = Flask(__name__)

AUTH_SERVER_URL = os.getenv('AUTH_SERVER_URL_DOCKER')
if not AUTH_SERVER_URL:
    AUTH_SERVER_URL = os.getenv('AUTH_SERVER_URL_LOCAL')


def validate_access_token(access_token: str) -> bool:
    """
    Send an access token to the Auth Server's /verify_token endpoint for validation.
    Returns True if the token is valid, False otherwise.
    """
    data = {'access_token': access_token}

    response = requests.post(f'{AUTH_SERVER_URL}/verify_token', json=data)

    return response.status_code == 200


@app.route('/get_data', methods=['POST'])
def get_data():
    """
    This endpoint is used to retrieve the secret data.
    Requires a valid access token for authentication in the request body.
    Returns the requested data if the access token is valid; otherwise, returns an error response.
    """
    data = request.get_json()
    access_token = data.get('access_token', None)

    if not access_token:
        print('Access token is missing, 400')
        return jsonify({'message': 'Access token is missing', 'success': False}), 400

    if validate_access_token(access_token):
        # Access token is valid, return the requested data
        requested_data = {
            'secret_data': 'The secret is that you are a robot : )',
            'success': True
        }
        print('Access token is valid, returning the requested data, 200')
        return jsonify(requested_data), 200

    else:
        # Access token is invalid
        print('Unauthorized, 401')
        return jsonify({'message': 'Unauthorized', 'success': False}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
