import base64
import hashlib
import random
from datetime import datetime
from typing import Optional

import requests
from requests import Response

from blogs.hatena.blog_entry_response_parser import parse_blog_entries_xml, get_next_page_url, parse_blog_entry_xml
from blogs.hatena.photo_entry_response_parser import parse_photo_entry_xml
from blogs.hatena.templates.hatena_entry_format import build_hatena_blog_entry_xml_body, get_summary_page_title, \
    build_hatena_photo_entry_xml_body
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.blog.photo_entry import PhotoEntry
from file.blog_config import BlogConfig
from file.file_accessor import read_pic_file_b64
from file.files_operator import get_file_name_from_file_path
from ltime.time_resolver import resolve_current_time_sequence

HATENA_BLOG_ENTRY_API = 'https://blog.hatena.ne.jp/{HATENA_ID}/{BLOG_ID}/atom/entry'
HATENA_PHOTO_ENTRY_POST_API = 'https://f.hatena.ne.jp/atom/post'
HATENA_PHOTO_ENTRY_EDIT_API = 'https://f.hatena.ne.jp/atom/edit'


def build_wsse(blog_config: BlogConfig):
    user_name = blog_config.hatena_id
    api_key = blog_config.api_key
    created_time = datetime.now().isoformat() + "Z"
    b_nonce = hashlib.sha1(str(random.random()).encode()).digest()
    b_password_digest = hashlib.sha1(b_nonce + created_time.encode() + api_key.encode()).digest()
    wsse = f'UsernameToken Username={user_name}, ' + \
           f'PasswordDigest={base64.b64encode(b_password_digest).decode()}, ' + \
           f'Nonce={base64.b64encode(b_nonce).decode()}, ' + \
           f'Created={created_time}'
    return wsse


# Todo: OAuth
def __build_request_header(blog_config: BlogConfig):
    # 'Accept': 'application/xml',
    # 'Content-Type': 'application/xml',
    return {
        'X-WSSE': build_wsse(blog_config)
    }


def __build_hatena_blog_AtomPub_api_base_url(blog_config: BlogConfig) -> str:
    api_url = HATENA_BLOG_ENTRY_API. \
        replace('{HATENA_ID}', blog_config.hatena_id).replace('{BLOG_ID}', blog_config.blog_id)
    return api_url


def __build_hatena_photo_entry_body(image_file_path: str) -> Optional[str]:
    __PIC_EXTENSION_TO_CONTENT_TYPE = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'svg': 'image/svg+xml',
    }
    split_str = image_file_path.rsplit('.', 1)
    title = f'{resolve_current_time_sequence()}_{get_file_name_from_file_path(split_str[0])}'
    extension = split_str[1].lower()
    if not extension in __PIC_EXTENSION_TO_CONTENT_TYPE:
        return None
    b64_pic_data = read_pic_file_b64(image_file_path)
    return build_hatena_photo_entry_xml_body(title, __PIC_EXTENSION_TO_CONTENT_TYPE[extension], b64_pic_data)


def __resolve_blog_entry_response_xml_data(xml_string_opt: Optional[str]) -> Optional[BlogEntry]:
    if xml_string_opt is None:
        return None
    return parse_blog_entry_xml(xml_string_opt)


def __resolve_photo_entry_response_xml_data(xml_string_opt: Optional[str], image_file_path: str) \
        -> Optional[PhotoEntry]:
    if xml_string_opt is None:
        return None
    return parse_photo_entry_xml(xml_string_opt, image_file_path)


# GET Blog
def execute_get_hatena_specified_blog_entry_api(blog_config: BlogConfig, entry_id: str) -> Optional[BlogEntry]:
    api_url = f'{__build_hatena_blog_AtomPub_api_base_url(blog_config)}/{entry_id}'
    request_headers = __build_request_header(blog_config)
    xml_string_opt = execute_get_api(api_url, request_headers)
    return __resolve_blog_entry_response_xml_data(xml_string_opt)


def execute_get_hatena_all_entry_api(blog_config: BlogConfig) -> Optional[BlogEntries]:
    api_url = __build_hatena_blog_AtomPub_api_base_url(blog_config)
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


# GET Photo
def execute_get_hatena_specified_photo_entry_api(blog_config: BlogConfig, entry_id: str) -> Optional[PhotoEntry]:
    api_url = f'{HATENA_PHOTO_ENTRY_EDIT_API}/{entry_id}'
    request_headers = __build_request_header(blog_config)
    xml_string_opt = execute_get_api(api_url, request_headers)
    return __resolve_photo_entry_response_xml_data(xml_string_opt, '')


# PUT blog
def __execute_put_hatena_blog_entry_update_api(blog_config: BlogConfig, url: str, title: str, category: str,
                                               content: str) \
        -> Optional[str]:
    body = build_hatena_blog_entry_xml_body(blog_config, title, category, content)
    return execute_put_api(url, __build_request_header(blog_config), body.encode(encoding='utf-8'))


def execute_put_hatena_summary_page(blog_config: BlogConfig, content: str) -> bool:
    url = f'{__build_hatena_blog_AtomPub_api_base_url(blog_config)}/{blog_config.summary_entry_id}'
    category = 'Summary'
    res = __execute_put_hatena_blog_entry_update_api(blog_config, url, get_summary_page_title(), category, content)
    if res is None:
        return False
    return True


def execute_put_hatena_blog_update_api(blog_config: BlogConfig, entry_id: str, title: str, category: str,
                                       content: str) -> Optional[BlogEntry]:
    url = f'{__build_hatena_blog_AtomPub_api_base_url(blog_config)}/{entry_id}'
    xml_string_opt = __execute_put_hatena_blog_entry_update_api(blog_config, url, title, category, content)
    return __resolve_blog_entry_response_xml_data(xml_string_opt)


# PUT photo
def execute_put_hatena_photo_update_api(blog_config: BlogConfig, image_file_path: str):
    """
    画像更新API実行。このAPIを実行するとローカルで管理している画像の更新時間も更新される
    :param blog_config:
    :param image_file_path:
    :return:
    """
    url = HATENA_PHOTO_ENTRY_EDIT_API
    body = __build_hatena_photo_entry_body(image_file_path)
    xml_string_opt = execute_put_api(url, __build_request_header(blog_config), body.encode(encoding='utf-8'))
    image_filename = get_file_name_from_file_path(image_file_path)
    return __resolve_photo_entry_response_xml_data(xml_string_opt, image_filename)


# POST blog
def execute_post_hatena_blog_register_api(blog_config: BlogConfig, title: str, category: str, content: str) \
        -> Optional[BlogEntry]:
    url = __build_hatena_blog_AtomPub_api_base_url(blog_config)
    body = build_hatena_blog_entry_xml_body(blog_config, title, category, content)
    xml_string_opt = execute_post_api(url, __build_request_header(blog_config), body.encode(encoding='utf-8'))
    return __resolve_blog_entry_response_xml_data(xml_string_opt)


# POST photo
def execute_post_hatena_photo_register_api(blog_config: BlogConfig, image_file_path: str):
    url = HATENA_PHOTO_ENTRY_POST_API
    body = __build_hatena_photo_entry_body(image_file_path)
    xml_string_opt = execute_post_api(url, __build_request_header(blog_config), body)
    image_filename = get_file_name_from_file_path(image_file_path)
    return __resolve_photo_entry_response_xml_data(xml_string_opt, image_filename)


# common executor
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
