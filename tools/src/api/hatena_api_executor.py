import base64
import hashlib
import random
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from api.response_parser import parse_blog_entries_xml, get_next_page_url, parse_blog_entry_xml
from domain.blog_entry import BlogEntries, BlogEntry
from file.blog_config import BlogConfig
from templates.hatena_entry_format import build_hatena_entry_xml_body, get_summary_page_title

HATENA_BASEURL = 'https://blog.hatena.ne.jp'
HATENA_BLOG_ENTRY_API = HATENA_BASEURL + '/{HATENA_ID}/{BLOG_ID}/atom/entry'


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
        'X-WSSE': f'UsernameToken Username={user_name}, ' +
                  f'PasswordDigest={base64.b64encode(b_password_digest).decode()}, ' +
                  f'Nonce={base64.b64encode(b_nonce).decode()}, ' +
                  f'Created={created_time}'
    }


def build_hatena_AtomPub_api_base_url(blog_config: BlogConfig) -> str:
    api_url = HATENA_BLOG_ENTRY_API. \
        replace('{HATENA_ID}', blog_config.hatena_id).replace('{BLOG_ID}', blog_config.blog_id)
    return api_url


def execute_get_hatena_specified_entry_api(blog_config: BlogConfig, entry_id: str) -> BlogEntry:
    api_url = f'{build_hatena_AtomPub_api_base_url(blog_config)}/{entry_id}'
    request_headers = build_request_header(blog_config)
    xml_string = execute_get_api(api_url, request_headers)
    return parse_blog_entry_xml(xml_string)


def execute_get_hatena_all_entry_api(blog_config: BlogConfig) -> BlogEntries:
    api_url = build_hatena_AtomPub_api_base_url(blog_config)
    request_headers = build_request_header(blog_config)
    xml_string = execute_get_api(api_url, request_headers)
    blog_entries = parse_blog_entries_xml(xml_string, blog_config)

    next_url = get_next_page_url(xml_string)
    while next_url is not None:
        next_xml_string = execute_get_api(next_url, request_headers)
        next_blog_entries = parse_blog_entries_xml(next_xml_string, blog_config)
        next_url = get_next_page_url(next_xml_string)
        blog_entries.merge(next_blog_entries)
    return blog_entries


def execute_put_hatena_summary_entry(blog_config: BlogConfig, content):
    url = build_hatena_AtomPub_api_base_url(blog_config) + '/' + blog_config.summary_entry_id
    category = 'Summary'
    execute_put_hatena_entry_update_api(blog_config, url, get_summary_page_title(), category, content)


def execute_put_hatena_entry_update_api(blog_config: BlogConfig, url: str, title: str, category: str, content: str):
    body = build_hatena_entry_xml_body(blog_config, title, category, content)
    execute_put_api(url, build_request_header(blog_config), body.encode(encoding='utf-8'))


def execute_get_api(url: str, headers: object) -> str:
    response = requests.get(url, headers=headers)
    print(response.status_code, response.reason, 'GET', url)
    if response.status_code == 200:
        return response.text  # format: xml
    else:
        raise Exception(f'api failure: url={url} headers={headers}')


def execute_put_api(url: str, headers: object, body):
    response = requests.put(url, headers=headers, data=body)
    print(response.status_code, response.reason, 'PUT', url)
    if response.status_code != 200 and response.status_code != 201:
        print('body: ' + response.text)
    else:
        print('SUCCESS')


def execute_post_api(url: str, headers: object, body):
    response = requests.post(url, headers=headers, data=body)
    print(response.status_code, response.reason, 'POST', url)
    if response.status_code != 200 and response.status_code != 201:
        print('body: ' + response.text)
    else:
        print('SUCCESS')
