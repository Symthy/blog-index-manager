from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from common.constant import HATENA_BLOG_ENTRY_LIST_PATH, HATENA_BLOG_ENTRY_DUMP_DIR, NON_CATEGORY_OTHERS
from domain.data_dumper import dump_entry_data, resolve_dump_field_data
from domain.interface import IEntries, IEntry
from file.file_accessor import dump_json, load_json
from ltime.time_resolver import resolve_entry_current_time, convert_datetime_to_entry_time_str, \
    convert_datetime_to_month_day_str


class BlogEntry(IEntry):
    def __init__(self, entry_id: str, title: str, content: str, url: str, api_url: str,
                 last_updated: Optional[datetime], categories: List[str], docs_id: Optional[str] = None):
        self.__id = entry_id
        self.__title = title
        self.__content = content
        self.__url = url
        self.__api_url = api_url
        self.__last_updated: Optional[datetime] = last_updated  # Make it optional just in case
        self.__categories = categories
        self.__local_docs_id = docs_id  # Todo

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
        return convert_datetime_to_entry_time_str(self.__last_updated)

    @property
    def last_updated_month_day(self) -> str:
        return convert_datetime_to_month_day_str(self.__last_updated)

    @property
    def categories(self) -> List[str]:
        return self.__categories

    def resolve_category(self) -> str:
        if len(self.__categories) == 0:
            return NON_CATEGORY_OTHERS
        return self.__categories[0]

    @property
    def local_docs_id(self):
        return self.__local_docs_id

    @property
    def local_dir_path(self):
        return ""  # TODO

    @property
    def pictures(self):
        return {}  # TODO

    def build_id_to_title(self) -> Dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.url}) ({self.last_updated_month_day})'

    def build_dump_data(self, json_data: Optional[object] = None) -> object:
        return {
            "id": resolve_dump_field_data(self, json_data, 'id'),
            "title": resolve_dump_field_data(self, json_data, 'title'),
            "top_category": resolve_dump_field_data(self, json_data, 'top_category'),
            "categories": resolve_dump_field_data(self, json_data, 'categories'),
            "url": resolve_dump_field_data(self, json_data, 'url'),
            "api_url": resolve_dump_field_data(self, json_data, 'api_url'),
            "last_updated": resolve_dump_field_data(self, json_data, 'last_updated'),
            "local_docs_id": resolve_dump_field_data(self, json_data, 'local_docs_id'),
            "local_dir_path": resolve_dump_field_data(self, json_data, 'local_dir_path'),
            "pictures": resolve_dump_field_data(self, json_data, 'pictures')
        }

    def dump_data(self, dump_file_path: str):
        dump_entry_data(self, dump_file_path)


class BlogEntries(IEntries):
    def __init__(self, entries: List[BlogEntry] = None):
        self.__entries: List[BlogEntry] = []
        if entries is not None:
            self.__entries: List[BlogEntry] = entries

    @property
    def entries(self) -> List[BlogEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def add_entry(self, blog_entry: BlogEntry):
        self.__entries.append(blog_entry)

    def merge(self, blog_entries: BlogEntries):
        self.__entries.extend(blog_entries.entries)

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    def dump_all_data(self, dump_file_path: str):
        json_data = load_json(dump_file_path)
        json_data['updated_time'] = resolve_entry_current_time()
        json_entries = {}
        if 'entries' in json_data:
            json_entries = json_data['entries']
        for entry in self.__entries:
            if not entry.id in json_entries:
                json_entries[entry.id] = entry.title
                entry.dump_data(f'{HATENA_BLOG_ENTRY_DUMP_DIR}/{entry.id}.json')
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
