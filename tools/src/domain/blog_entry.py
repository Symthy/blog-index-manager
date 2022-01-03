from __future__ import annotations

import os
from datetime import datetime
from typing import List, Optional

from domain.interface import IConvertibleMarkdownData
from file.file_accessor import dump_json, load_json
from ltime.time_resolver import resolve_entry_current_time, convert_entry_datetime_to_str


class BlogEntry:
    def __init__(self, entry_id: str, title: str, content: str, url: str, api_url: str,
                 last_updated: Optional[datetime], categories: List[str]):
        self.__id = entry_id
        self.__title = title
        self.__content = content
        self.__url = url
        self.__api_url = api_url
        # Make it optional just in case
        self.__last_updated: Optional[datetime] = last_updated
        self.__categories = categories

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def content(self):
        return self.__content

    @property
    def url(self):
        return self.__url

    @property
    def api_url(self):
        return self.__api_url

    @property
    def last_updated(self) -> str:
        return convert_entry_datetime_to_str(self.__last_updated)

    def get_updated_month_day(self) -> str:
        if self.__last_updated is None:
            return 'unknown'
        return self.__last_updated.strftime('%Y/%m')

    @property
    def top_category(self) -> str:
        if self.is_non_category():
            return 'Others'
        return self.__categories[0]

    @property
    def categories(self) -> List[str]:
        return self.__categories

    def is_non_category(self) -> bool:
        return len(self.__categories) <= 0

    @property
    def local_path(self):
        return ""  # TODO

    @property
    def pictures(self):
        return {}  # TODO

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.url}) ({self.get_updated_month_day()})'

    def build_dump_data(self, json_data=None) -> object:
        def resolve_field_data(entry, dump_data, field_name):
            if dump_data is None:
                return getattr(entry, field_name)
            if field_name in dump_data:
                return dump_data[field_name]
            return getattr(entry, field_name)

        return {
            "id": resolve_field_data(self, json_data, 'id'),
            "title": resolve_field_data(self, json_data, 'title'),
            "top_category": resolve_field_data(self, json_data, 'top_category'),
            "categories": resolve_field_data(self, json_data, 'categories'),
            "url": resolve_field_data(self, json_data, 'url'),
            "api_url": resolve_field_data(self, json_data, 'api_url'),
            "last_updated": resolve_field_data(self, json_data, 'last_updated'),
            "local_path": resolve_field_data(self, json_data, 'local_path'),  # TODO
            "pictures": resolve_field_data(self, json_data, 'pictures')  # TODO
        }

    def dump_blog_entry_data(self, dump_file_path: str):
        if os.path.exists(dump_file_path):
            json_data = load_json(dump_file_path)
            dump_data = self.build_dump_data(json_data)
            dump_json(dump_file_path, dump_data)
            return
        dump_json(dump_file_path, self.build_dump_data())


class BlogEntries(IConvertibleMarkdownData):
    def __init__(self, entries: List[BlogEntry] = None):
        self.__entries: List[BlogEntry] = []
        if entries is not None:
            self.__entries: List[BlogEntry] = entries

    @property
    def items(self) -> List[BlogEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def add_entry(self, blog_entry: BlogEntry):
        self.__entries.append(blog_entry)

    def add_entries(self, blog_entries: List[BlogEntry]):
        self.__entries.extend(blog_entries)

    def merge(self, blog_entries: BlogEntries):
        self.add_entries(blog_entries.items)

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    def dump_all_entry(self):
        HATENA_BLOG_ENTRY_DUMP_DIR = '../out/hatena_entry_data/'
        HATENA_BLOG_ENTRY_LIST_PATH = '../out/hatena_entry_list.json'

        json_data = load_json(HATENA_BLOG_ENTRY_LIST_PATH)
        json_data['updated_time'] = resolve_entry_current_time()
        json_entries = {}
        if 'entries' in json_data:
            json_entries = json_data['entries']
        for entry in self.__entries:
            if not entry.id in json_entries:
                json_entries[entry.title] = entry.id
                entry.dump_blog_entry_data(f'{HATENA_BLOG_ENTRY_DUMP_DIR}/{entry.id}.json')
        # dump data format
        # {
        #   "updated_time": "2022-01-02T03:04:05",
        #   "entries": {
        #     "entry_id": "entry title"
        #      :
        #   }
        # }
        json_data['entries'] = json_entries
        dump_json(HATENA_BLOG_ENTRY_LIST_PATH, json_data)
