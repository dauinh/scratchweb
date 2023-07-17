import requests
import re

CONF_URL = 'https://pressingly-account.onrender.com'

def get_user_info(token):
    access_token = token['access_token']
    userInfoEndpoint = f'{CONF_URL}/oauth/userinfo'
    userInfoResponse = requests.post(userInfoEndpoint,
                                    headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'})
    userInfoResponse = userInfoResponse.json()
    match = re.match(r"(.*)@", userInfoResponse['email'])
    username = match.group(1)
    return (username, userInfoResponse['email'])