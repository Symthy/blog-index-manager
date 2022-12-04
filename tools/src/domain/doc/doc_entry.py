from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from common.constant import NON_CATEGORY_GROUP_NAME
from domain.interface import IEntry, IEntries
from dump.entry_data_dumper import resolve_dump_field_data
from ltime.time_resolver import convert_datetime_to_month_day_str, convert_datetime_to_entry_time_str, \
    convert_entry_time_str_to_datetime


class DocEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_DIR_PATH = 'dir_path'
    FIELD_DOC_FILE_NAME = 'doc_file_name'
    FIELD_TOP_CATEGORY = 'top_category'
    FIELD_CATEGORIES = 'categories'
    FIELD_PICKUP = 'pickup'
    FIELD_CREATED_AT = 'created_at'
    FIELD_UPDATED_AT = 'updated_at'

    def __init__(self, docs_id: str, title: str, dir_path: str, doc_file_name: str, categories: List[str],
                 is_pickup: bool = False, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.__id = docs_id
        self.__title = title
        self.__dir_path = dir_path
        self.__doc_file_name = doc_file_name
        self.__top_category = categories[0] if not len(categories) == 0 else NON_CATEGORY_GROUP_NAME
        self.__categories = categories
        self.__pickup = is_pickup
        self.__created_at: Optional[datetime] = created_at
        self.__updated_at: Optional[datetime] = updated_at

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
    def doc_file_name(self):
        return self.__doc_file_name

    @property
    def categories(self):
        return self.__categories

    @property
    def top_category(self) -> str:
        return self.__top_category

    @property
    def is_pickup(self) -> bool:
        return self.__pickup

    @property
    def created_at(self) -> str:
        return convert_datetime_to_entry_time_str(self.__created_at)

    @property
    def updated_at(self) -> str:
        return convert_datetime_to_entry_time_str(self.__updated_at)

    @property
    def updated_at_month_day(self):
        return convert_datetime_to_month_day_str(self.__updated_at)

    def build_id_to_title(self) -> Dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.dir_path}{self.doc_file_name})'

    def build_dump_data(self, json_data=None) -> object:
        return {
            DocEntry.FIELD_ID: resolve_dump_field_data(self, json_data, DocEntry.FIELD_ID),
            DocEntry.FIELD_TITLE: resolve_dump_field_data(self, json_data, DocEntry.FIELD_TITLE),
            DocEntry.FIELD_DIR_PATH: resolve_dump_field_data(self, json_data, DocEntry.FIELD_DIR_PATH),
            DocEntry.FIELD_DOC_FILE_NAME: resolve_dump_field_data(self, json_data, DocEntry.FIELD_DOC_FILE_NAME),
            DocEntry.FIELD_TOP_CATEGORY: resolve_dump_field_data(self, json_data, DocEntry.FIELD_TOP_CATEGORY),
            DocEntry.FIELD_CATEGORIES: resolve_dump_field_data(self, json_data, DocEntry.FIELD_CATEGORIES),
            DocEntry.FIELD_PICKUP: resolve_dump_field_data(self, json_data, DocEntry.FIELD_PICKUP),
            DocEntry.FIELD_CREATED_AT: resolve_dump_field_data(self, json_data, DocEntry.FIELD_CREATED_AT),
            DocEntry.FIELD_UPDATED_AT: resolve_dump_field_data(self, json_data, DocEntry.FIELD_UPDATED_AT),
        }

    @classmethod
    def restore_from_json_data(cls, dump_json_data: Dict[str, any]) -> DocEntry:
        return DocEntry(
            dump_json_data[DocEntry.FIELD_ID],
            dump_json_data[DocEntry.FIELD_TITLE],
            dump_json_data[DocEntry.FIELD_DIR_PATH],
            dump_json_data[DocEntry.FIELD_DOC_FILE_NAME],
            dump_json_data[DocEntry.FIELD_CATEGORIES],
            # field added later
            dump_json_data[DocEntry.FIELD_PICKUP] if DocEntry.FIELD_PICKUP in dump_json_data else False,
            convert_entry_time_str_to_datetime(dump_json_data[DocEntry.FIELD_CREATED_AT]),
            convert_entry_time_str_to_datetime(dump_json_data[DocEntry.FIELD_UPDATED_AT])
        )


class DocEntries(IEntries):
    def __init__(self, entries: List[DocEntry] = None):
        # Todo: Need to consider later. Is it better to use dict? (low priority)
        self.__entries: List[DocEntry] = []
        if entries is not None:
            self.__entries: List[DocEntry] = entries

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if not len(self.__entries) == len(other.__entries):
            return False
        for entry in self.__entries:
            other_entry = other.get_entry(entry.id)
            if other_entry is None:
                return False
            if not entry.__dict__ == other_entry.__dict__:
                return False
        return True

    @property
    def entry_list(self) -> List[DocEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def is_contains(self, target_entry_id: str) -> bool:
        for entry in self.__entries:
            if entry.id == target_entry_id:
                return True
        return False

    def get_entry(self, entry_id) -> Optional[DocEntry]:
        for entry in self.__entries:
            if entry.id == entry_id:
                return entry
        return None

    def get_pickup_entries(self) -> List[DocEntry]:
        pickup_entries: List[DocEntry] = []
        for entry in self.__entries:
            if entry.is_pickup:
                pickup_entries.append(entry)
        return pickup_entries

    def __add_entry(self, blog_entry: DocEntry):
        self.__entries.append(blog_entry)

    def __add_entries(self, blog_entries: List[DocEntry]):
        self.__entries.extend(blog_entries)

    def merge(self, docs_entries: DocEntries):
        # existed entry is overwrite
        self.__add_entries(docs_entries.entry_list)

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    @classmethod
    def new_instance(cls, entry_list: List[DocEntry]) -> DocEntries:
        return DocEntries(entry_list)
