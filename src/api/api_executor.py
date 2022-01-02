import base64
import hashlib
import random
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from file.blog_config import BlogConfig

HATENA_BASEURL = 'https://blog.hatena.ne.jp'
HATENA_GET_BLOG_ENTRY_LIST_API = HATENA_BASEURL + '/{HATENA_ID}/{BLOG_ID}/atom/entry'


# Todo: OAuth
def build_request_header(blog_config: BlogConfig):
    user_name = blog_config.hatena_id
    api_key = blog_config.api_key
    created_time = datetime.now().isoformat() + "Z"
    b_nonce = hashlib.sha1(str(random.random()).encode()).digest()
    b_password_digest = hashlib.sha1(b_nonce + created_time.encode() + api_key.encode()).digest()
    return {
        'Accept': 'application/xml',
        'Content-Type': 'application/xml',
        'X-WSSE': f'UsernameToken Username={user_name}, PasswordDigest={base64.b64encode(b_password_digest).decode()}, ' +
                  f'Nonce={base64.b64encode(b_nonce).decode()}, Created={created_time}'
    }


def build_hatena_AtomPub_api_base_url(blog_config: BlogConfig) -> str:
    api_url = HATENA_GET_BLOG_ENTRY_LIST_API. \
        replace('{HATENA_ID}', blog_config.hatena_id).replace('{BLOG_ID}', blog_config.blog_id)
    return api_url


def execute_get_entry_list_api(blog_config: BlogConfig) -> ET.Element:
    api_url = build_hatena_AtomPub_api_base_url(blog_config)
    xml_string = execute_get_api(api_url, build_request_header(blog_config))
    root = ET.fromstring(xml_string)
    return root


def execute_get_api(url: str, headers: object) -> str:
    response = requests.get(url, headers=headers)
    print(response.status_code, response.reason, url)
    if response.status_code == 200:
        return response.text  # format: xml
    else:
        raise Exception(f'api failure: url={url} headers={headers}')
