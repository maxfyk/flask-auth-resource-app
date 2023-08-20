import requests

AUTH_SERVER_URL = 'http://localhost:5001'


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


def main(username, password):
    # Get an access token
    access_token = get_access_token(username, password)
    if not access_token:
        print('Authorization failed...')
        return

    print('Authorization successful!')
    print(f'Access token: {access_token}')

    # Make a request to the protected service
    # response = client.get_data()
    # print(response)


if __name__ == '__main__':
    main(username='admin', password='Kpj8q42890889')
