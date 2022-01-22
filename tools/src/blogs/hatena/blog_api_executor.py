import base64
import hashlib
import random
from datetime import datetime
from typing import Optional

from requests import Response

from blogs.api.api_executor import execute_get_api, execute_put_api, execute_post_api, execute_delete_api
from blogs.api.interface import IBlogApiExecutor
from blogs.hatena.blog_entry_response_parser import parse_blog_entries_xml, get_next_page_url, parse_blog_entry_xml
from blogs.hatena.photo_entry_response_parser import parse_photo_entry_xml
from blogs.hatena.templates.hatena_entry_format import build_hatena_blog_entry_xml_body, get_summary_page_title, \
    build_hatena_photo_entry_post_xml_body
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.blog.photo_entry import PhotoEntry
from files.conf.blog_config import BlogConfig
from files.file_accessor import read_pic_file_b64
from files.files_operator import get_file_name_from_file_path
from ltime.time_resolver import resolve_current_time_sequence

HATENA_BLOG_ENTRY_API = 'https://blog.hatena.ne.jp/{HATENA_ID}/{BLOG_ID}/atom/entry'
HATENA_PHOTO_ENTRY_POST_API = 'https://f.hatena.ne.jp/atom/post'
HATENA_PHOTO_ENTRY_EDIT_API = 'https://f.hatena.ne.jp/atom/edit'


class HatenaBlogApiExecutor(IBlogApiExecutor):
    def __init__(self, blog_config: BlogConfig):
        self.__blog_conf = blog_config

    def __build_hatena_blog_AtomPub_api_base_url(self) -> str:
        api_url = HATENA_BLOG_ENTRY_API. \
            replace('{HATENA_ID}', self.__blog_conf.hatena_id).replace('{BLOG_ID}', self.__blog_conf.blog_id)
        return api_url

    # Todo: OAuth
    # public: for testing
    def build_request_header(self):
        def __build_wsse(blog_config: BlogConfig):
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

        # 'Accept': 'application/xml',
        # 'Content-Type': 'application/xml',
        return {
            'X-WSSE': __build_wsse(self.__blog_conf)
        }

    # common api executor
    @classmethod
    def __resolve_api_response(cls, http_method: str, response: Response, url: str) -> Optional[str]:
        print(response.status_code, response.reason, http_method, url)
        if response.status_code == 200 or response.status_code == 201:
            print('SUCCESS')
            return response.text  # format: xml
        else:
            print(f'[Error] API failure: body={response.text} url={url}')
            return None

    # Blog
    # GET Blog
    def execute_get_blog_entry_api(self, entry_id: str) -> Optional[BlogEntry]:
        api_url = f'{self.__build_hatena_blog_AtomPub_api_base_url()}/{entry_id}'
        request_headers = self.build_request_header()
        xml_string_opt = execute_get_api(api_url, request_headers, HatenaBlogApiExecutor.__resolve_api_response)
        return parse_blog_entry_xml(xml_string_opt)

    def execute_get_all_blog_entries_api(self) -> BlogEntries:
        next_url = self.__build_hatena_blog_AtomPub_api_base_url()
        request_headers = self.build_request_header()
        blog_entries = BlogEntries()
        while next_url is not None:
            xml_string_opt = execute_get_api(next_url, request_headers,
                                             HatenaBlogApiExecutor.__resolve_api_response)
            if xml_string_opt is None:
                break
            next_blog_entries = parse_blog_entries_xml(xml_string_opt, self.__blog_conf.summary_entry_id)
            next_url = get_next_page_url(xml_string_opt)
            blog_entries.merge(next_blog_entries)
        return blog_entries

    # POST blog
    def execute_register_blog_entry_api(self, title: str, category: str, content: str) -> Optional[BlogEntry]:
        url = self.__build_hatena_blog_AtomPub_api_base_url()
        body = build_hatena_blog_entry_xml_body(self.__blog_conf.hatena_id, title, category, content)
        headers = self.build_request_header()
        print('[Info] API execute: POST Blog')
        xml_string_opt = execute_post_api(url, headers, body.encode(encoding='utf-8'),
                                          HatenaBlogApiExecutor.__resolve_api_response)
        return parse_blog_entry_xml(xml_string_opt)

    # PUT blog
    def __execute_put_blog_entry_api(self, url: str, title: str, category: str,
                                     content: str) -> Optional[str]:
        body = build_hatena_blog_entry_xml_body(self.__blog_conf.hatena_id, title, category, content)
        print('[Info] API execute: PUT Blog')
        return execute_put_api(url, self.build_request_header(), body.encode(encoding='utf-8'),
                               HatenaBlogApiExecutor.__resolve_api_response)

    def execute_update_blog_summary_page(self, content: str) -> bool:
        url = f'{self.__build_hatena_blog_AtomPub_api_base_url()}/{self.__blog_conf.summary_entry_id}'
        category = 'Summary'
        res = self.__execute_put_blog_entry_api(url, get_summary_page_title(), category, content)
        if res is None:
            return False
        return True

    def execute_update_blog_entry_api(self, entry_id: str, title: str, category: str,
                                      content: str) -> Optional[BlogEntry]:
        url = f'{self.__build_hatena_blog_AtomPub_api_base_url()}/{entry_id}'
        xml_string_opt = self.__execute_put_blog_entry_api(url, title, category, content)
        return parse_blog_entry_xml(xml_string_opt)

    # GET Photo
    def execute_get_photo_entry_api(self, entry_id: str) -> Optional[PhotoEntry]:
        api_url = f'{HATENA_PHOTO_ENTRY_EDIT_API}/{entry_id}'
        request_headers = self.build_request_header()
        print('[Info] API execute: GET Photo')
        xml_string_opt = execute_get_api(api_url, request_headers, HatenaBlogApiExecutor.__resolve_api_response)
        return parse_photo_entry_xml(xml_string_opt, '')

    # POST photo
    def execute_register_photo_entry_api(self, image_file_path: str) -> Optional[PhotoEntry]:
        def __build_hatena_photo_entry_body() -> Optional[str]:
            # Todo: refactor use library
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
            return build_hatena_photo_entry_post_xml_body(title, __PIC_EXTENSION_TO_CONTENT_TYPE[extension],
                                                          b64_pic_data)

        url = HATENA_PHOTO_ENTRY_POST_API
        body = __build_hatena_photo_entry_body()
        print('[Info] API execute: POST Photo')
        xml_string_opt = execute_post_api(url, self.build_request_header(), body,
                                          HatenaBlogApiExecutor.__resolve_api_response)
        image_filename = get_file_name_from_file_path(image_file_path)
        return parse_photo_entry_xml(xml_string_opt, image_filename)

    # UPDATE(DELETE+POST) photo
    # PUT can change title only
    def execute_update_photo_entry_api(self, image_file_path: str, photo_entry: PhotoEntry) -> Optional[PhotoEntry]:
        headers = self.build_request_header()
        print('[Info] API execute: DELETE Photo')
        url = f'{HATENA_PHOTO_ENTRY_EDIT_API}/{photo_entry.id}'
        execute_delete_api(url, headers, HatenaBlogApiExecutor.__resolve_api_response)
        return self.execute_register_photo_entry_api(image_file_path)
