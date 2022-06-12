import configparser
import urllib.parse
import webbrowser

import requests
from requests_oauthlib import OAuth1

from blogs.hatena.blog_api_executor import HatenaBlogApiExecutor
from files.conf.blog_config import BlogConfig

API_SCOPE = ['read_public']

REQUEST_URL = 'https://www.hatena.com/oauth/initiate'
AUTHORIZE_URL = 'https://www.hatena.ne.jp/oauth/authorize'
ACCESS_TOKEN_URL = 'https://www.hatena.com/oauth/token'
CALLBACK_URI = 'oob'

GET_BOOKMARKS_URL = 'https://b.hatena.ne.jp/my/search/json'


# Todo: refactor because try code
class RequestToken:
    def __init__(self, data: dict[str, str]):
        self.oauth_token = data['oauth_token']
        self.oauth_token_secret = data['oauth_token_secret']
        self.oauth_callback_confirmed = data['oauth_callback_confirmed']


class AccessToken:
    def __init__(self, data: dict[str, str]):
        self.oauth_token = data['oauth_token']
        self.oauth_token_secret = data['oauth_token_secret']
        self.url_name = data['url_name']
        self.display_name = data['display_name']


def execute_oauth(conf: BlogConfig):
    request_token = get_request_token(conf)
    redirect_auth_url(request_token)
    access_token = get_access_token(conf, request_token)
    write_config(access_token)


def get_request_token(conf: BlogConfig) -> RequestToken:
    auth = OAuth1(
        conf.oauth_api_key,
        conf.oauth_client_secret_key,
        callback_uri=CALLBACK_URI)
    res = requests.post(f'{REQUEST_URL}?scope=read_public', auth=auth)
    print(res.text)
    request_token = dict(urllib.parse.parse_qsl(res.text))
    return RequestToken(request_token)


def redirect_auth_url(request_token: RequestToken):
    webbrowser.open(f'{AUTHORIZE_URL}?oauth_token={request_token.oauth_token}')


def get_access_token(conf: BlogConfig, request_token: RequestToken) -> AccessToken:
    oauth_verifier = input("input code:")
    auth = OAuth1(
        conf.oauth_api_key,
        conf.oauth_client_secret_key,
        request_token.oauth_token,
        request_token.oauth_token_secret,
        verifier=oauth_verifier)
    res = requests.post(ACCESS_TOKEN_URL, auth=auth)

    access_token = dict(urllib.parse.parse_qsl(res.text))
    print(access_token)
    return AccessToken(access_token)


def write_config(access_token: AccessToken):
    config = configparser.RawConfigParser()
    section = 'HATENA'
    config.add_section(section)
    config.set(section, 'TOKEN', access_token.oauth_token)
    config.set(section, 'TOKEN_SECRET', access_token.oauth_token_secret)
    with open('./conf/access_token.conf', 'w') as file:
        config.write(file)


def get_hatena_bookmarks(conf: BlogConfig):
    config = configparser.ConfigParser()
    config.read('./conf/access_token.conf')
    section = 'HATENA'
    token = config.get(section, 'TOKEN')
    token_secret = config.get(section, 'TOKEN_SECRET')
    # Oauth認証ではうまくいかず
    auth = OAuth1(
        conf.oauth_api_key,
        conf.oauth_client_secret_key,
        token,
        token_secret)
    hatena = HatenaBlogApiExecutor(conf)
    headers = hatena.build_request_header()
    # res = requests.get(GET_BOOKMARKS_URL, auth=auth)
    res = requests.get(f'{GET_BOOKMARKS_URL}?q=all&limit=100', headers=headers)
    print(res.status_code, res.text)
