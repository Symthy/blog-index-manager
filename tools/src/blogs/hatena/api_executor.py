import base64
import hashlib
import random
from datetime import datetime
from typing import Optional

import requests
from requests import Response

from blogs.hatena.response_parser import parse_blog_entries_xml, get_next_page_url, parse_blog_entry_xml
from domain.blog_entry import BlogEntries, BlogEntry
from file.blog_config import BlogConfig
from templates.hatena_entry_format import build_hatena_entry_xml_body, get_summary_page_title

HATENA_BASEURL = 'https://blog.hatena.ne.jp'
HATENA_BLOG_ENTRY_API = HATENA_BASEURL + '/{HATENA_ID}/{BLOG_ID}/atom/entry'


# Todo: OAuth
def __build_request_header(blog_config: BlogConfig):
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


def __build_hatena_AtomPub_api_base_url(blog_config: BlogConfig) -> str:
    api_url = HATENA_BLOG_ENTRY_API. \
        replace('{HATENA_ID}', blog_config.hatena_id).replace('{BLOG_ID}', blog_config.blog_id)
    return api_url


def __resolve_response_xml_data(xml_string_opt: Optional[str]) -> Optional[BlogEntry]:
    if xml_string_opt is None:
        return None
    return parse_blog_entry_xml(xml_string_opt)


def execute_get_hatena_specified_entry_api(blog_config: BlogConfig, entry_id: str) -> Optional[BlogEntry]:
    api_url = f'{__build_hatena_AtomPub_api_base_url(blog_config)}/{entry_id}'
    request_headers = __build_request_header(blog_config)
    xml_string_opt = execute_get_api(api_url, request_headers)
    return __resolve_response_xml_data(xml_string_opt)


def execute_get_hatena_all_entry_api(blog_config: BlogConfig) -> Optional[BlogEntries]:
    api_url = __build_hatena_AtomPub_api_base_url(blog_config)
    request_headers = __build_request_header(blog_config)
    xml_string_opt = execute_get_api(api_url, request_headers)
    if xml_string_opt is None:
        return None
    blog_entries = parse_blog_entries_xml(xml_string_opt, blog_config)

    next_url = get_next_page_url(xml_string_opt)
    while next_url is not None:
        next_xml_string_opt = execute_get_api(next_url, request_headers)
        if next_xml_string_opt is None:
            break
        next_blog_entries = parse_blog_entries_xml(next_xml_string_opt, blog_config)
        next_url = get_next_page_url(next_xml_string_opt)
        blog_entries.merge(next_blog_entries)
    return blog_entries


def __execute_put_hatena_entry_update_api(blog_config: BlogConfig, url: str, title: str, category: str, content: str) \
        -> Optional[str]:
    body = build_hatena_entry_xml_body(blog_config, title, category, content)
    return execute_put_api(url, __build_request_header(blog_config), body.encode(encoding='utf-8'))


def execute_put_hatena_summary_page(blog_config: BlogConfig, content: str) -> bool:
    url = f'{__build_hatena_AtomPub_api_base_url(blog_config)}/{blog_config.summary_entry_id}'
    category = 'Summary'
    res = __execute_put_hatena_entry_update_api(blog_config, url, get_summary_page_title(), category, content)
    if res is None:
        return False
    return True


def execute_put_hatena_entry_update_api(blog_config: BlogConfig, entry_id: str, title: str, category: str,
                                        content: str) -> Optional[BlogEntry]:
    url = f'{__build_hatena_AtomPub_api_base_url(blog_config)}/{entry_id}'
    xml_string_opt = __execute_put_hatena_entry_update_api(blog_config, url, title, category, content)
    return __resolve_response_xml_data(xml_string_opt)


def execute_post_hatena_entry_register_api(blog_config: BlogConfig, title: str, category: str, content: str) \
        -> Optional[BlogEntry]:
    url = __build_hatena_AtomPub_api_base_url(blog_config)
    body = build_hatena_entry_xml_body(blog_config, title, category, content)
    xml_string_opt = execute_post_api(url, __build_request_header(blog_config), body.encode(encoding='utf-8'))
    return __resolve_response_xml_data(xml_string_opt)


def __resolve_api_response(http_method: str, response: Response, url: str, headers: object) -> Optional[str]:
    print(response.status_code, response.reason, http_method, url)
    if response.status_code == 200 or response.status_code == 201:
        print('SUCCESS')
        return response.text  # format: xml
    else:
        print(f'[Error] API failure: body={response.text} url={url} headers={headers}')
        return None


def execute_get_api(url: str, headers: object) -> Optional[str]:
    response = requests.get(url, headers=headers)
    return __resolve_api_response('GET', response, url, headers)


def execute_put_api(url: str, headers: object, body) -> Optional[str]:
    response = requests.put(url, headers=headers, data=body)
    return __resolve_api_response('PUT', response, url, headers)


def execute_post_api(url: str, headers: object, body) -> Optional[str]:
    response = requests.post(url, headers=headers, data=body)
    return __resolve_api_response('POST', response, url, headers)
