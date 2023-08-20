import requests

AUTH_SERVER_URL = 'http://localhost:5001'
RESOURCE_API_URL = 'http://localhost:5000'


def get_access_token(username: str, password: str) -> [str, bool]:
    response = requests.post(
        f'{AUTH_SERVER_URL}/authorize',
        json={'username': username, 'password': password}
    )

    data = response.json()
    if not data['success']:
        print(response.status_code, data['message'])
        return False

    return data['access_token']


def get_data(access_token: str) -> [str, bool]:
    response = requests.post(
        f'{RESOURCE_API_URL}/get_data',
        json={'access_token': access_token}
    )

    data = response.json()
    print(data)
    if not data['success']:
        print(response.status_code, data['message'])
        return False

    return data['secret_data']


def main(username, password):
    # Get an access token
    access_token = get_access_token(username, password)
    if not access_token:
        print('Authorization failed...')
        return

    print('Authorization successful!')
    print(f'Access token: {access_token}\n')

    # Use the access token to get the secret data
    secret_data = get_data(access_token)
    if not secret_data:
        print('Failed to get the secret data...')
        return

    print('Successfully retrieved the secret data!')
    print(f'Data: {secret_data}')


if __name__ == '__main__':
    main(username='admin', password='Kpj8q42890889')
