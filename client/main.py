import requests

auth_server_url = "http://auth_server:5001"

# get access token
response = requests.post(
    f"{auth_server_url}/authorize",
    json={"username": "admin", "password": "Kpj8q42890889"}
)
access_token = response.json()['access_token']
print(access_token)
