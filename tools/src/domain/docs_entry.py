from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from common.constant import NON_CATEGORY_NAME, LOACL_DOCS_ENTRY_LIST_PATH
from domain.data_dumper import dump_entry_data, resolve_dump_field_data
from domain.interface import IEntry, IEntries
from file.file_accessor import load_json, dump_json
from ltime.time_resolver import convert_datetime_to_month_day_str, convert_entry_datetime_to_str, \
    resolve_entry_current_time


class DocsEntry(IEntry):
    def __init__(self, docs_id: str, title: str, dir_path: str, created_at: datetime,
                 updated_at: Optional[datetime], categories: List[str]):
        self.__id = docs_id
        self.__title = title
        self.__dir_path = dir_path
        self.__created_at: datetime = created_at
        self.__updated_at: Optional[datetime] = updated_at
        self.__categories = categories

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def dir_path(self):
        return self.__dir_path

    @property
    def top_category(self):
        if len(self.__categories) == 0:
            return NON_CATEGORY_NAME
        return self.__categories[0]

    @property
    def categories(self):
        return self.__categories

    @property
    def created_at(self):
        return convert_entry_datetime_to_str(self.__created_at)

    @property
    def updated_at(self):
        return convert_entry_datetime_to_str(self.__updated_at)

    @property
    def updated_at_month_day(self):
        return convert_datetime_to_month_day_str(self.__updated_at)

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.dir_path})'

    def build_dump_data(self, json_data=None) -> object:
        return {
            "id": resolve_dump_field_data(self, json_data, 'id'),
            "title": resolve_dump_field_data(self, json_data, 'title'),
            "dir_path": resolve_dump_field_data(self, json_data, 'dir_path'),
            "top_category": resolve_dump_field_data(self, json_data, 'top_category'),
            "categories": resolve_dump_field_data(self, json_data, 'categories'),
            "created_at": resolve_dump_field_data(self, json_data, 'created_at'),
            "updated_at": resolve_dump_field_data(self, json_data, 'updated_at'),
        }

    def dump_data(self, dump_file_path: str):
        dump_entry_data(self, dump_file_path)


class DocsEntries(IEntries):
    def __init__(self, entries: List[DocsEntry] = None):
        self.__entries: List[DocsEntry] = []
        if entries is not None:
            self.__entries: List[DocsEntry] = entries

    def get_entries(self) -> List[DocsEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def add_entry(self, blog_entry: DocsEntry):
        self.__entries.append(blog_entry)

    def add_entries(self, blog_entries: List[DocsEntry]):
        self.__entries.extend(blog_entries)

    def merge(self, docs_entries: DocsEntries):
        self.add_entries(docs_entries.get_entries())

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    def dump_all_data(self, dump_file_path: str):
        json_data = load_json(dump_file_path)
        json_data['updated_time'] = resolve_entry_current_time()
        json_entries = {}
        if 'entries' in json_data:
            json_entries = json_data['entries']
        # Todo: grouping data dump
        # dump data format
        # {
        #   "updated_time": "2022-01-02T03:04:05",
        #   "entries": {
        #     "id": "title"
        #      :
        #   }
        # }
        json_data['entries'] = json_entries
        dump_json(LOACL_DOCS_ENTRY_LIST_PATH, json_data)
