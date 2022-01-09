from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from common.constant import NON_CATEGORY_GROUP_NAME, LOCAL_DOCS_ENTRY_LIST_PATH, CATEGORY_FILE_NAME, \
    LOCAL_DOCS_ENTRY_DUMP_DIR, ID_FILE_NAME_HEADER
from domain.data_dumper import dump_entry_data, resolve_dump_field_data
from domain.interface import IEntry, IEntries
from file.file_accessor import load_json, dump_json, read_text_file, is_exist_in_local_entry_list, write_text_line, \
    get_doc_title_from_md_file
from file.files_operator import get_md_file_path_in_target_dir, get_id_from_id_file, \
    get_files_name_from_path
from ltime.time_resolver import convert_datetime_to_month_day_str, convert_datetime_to_entry_time_str, \
    get_current_datetime, convert_datetime_to_time_sequence, \
    convert_entry_time_str_to_datetime


def new_doc_entries(move_from_path_to_move_to_path_dict: Dict[str, str]) -> DocEntries:
    docs_entry_list = []
    for move_from_path, move_to_path in move_from_path_to_move_to_path_dict.items():
        docs_entry_opt = new_doc_entry(move_from_path, move_to_path)
        if docs_entry_opt is not None:
            docs_entry_list.append(docs_entry_opt)
    return DocEntries(docs_entry_list)


def new_doc_entry(target_dir_path: str, move_to_path: str) -> Optional[DocEntry]:
    created_datetime: datetime = get_current_datetime()
    md_file_path = get_md_file_path_in_target_dir(target_dir_path)
    dir_name = get_files_name_from_path(target_dir_path)
    file_name = get_files_name_from_path(md_file_path)
    if md_file_path is None:
        print(f'[Error] skip: non exist md file (dir: {dir_name})')
        return None
    doc_title = get_doc_title_from_md_file(md_file_path)
    if doc_title is None:
        print(f'[Error] skip: empty doc title (dir: {dir_name})')
        return None
    entry_id: Optional[str] = get_id_from_id_file(target_dir_path)
    if entry_id is None:
        entry_id = convert_datetime_to_time_sequence(created_datetime)
        id_file_path = f'{target_dir_path}/{ID_FILE_NAME_HEADER}{entry_id}'
        write_text_line(id_file_path, entry_id)
    categories = read_text_file(target_dir_path + CATEGORY_FILE_NAME)
    created_at = created_datetime
    updated_at = None
    if is_exist_in_local_entry_list(entry_id):
        created_at = None  # use time in dump file
        updated_at = get_current_datetime()
    return DocEntry(entry_id, doc_title, move_to_path, file_name, categories, created_at, updated_at)


class DocEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_DIR_PATH = 'dir_path'
    FIELD_DOC_FILE = 'doc_file'
    FIELD_TOP_CATEGORY = 'top_category'
    FIELD_CATEGORIES = 'categories'
    FIELD_CREATED_AT = 'created_at'
    FIELD_UPDATED_AT = 'updated_at'

    def __init__(self, docs_id: str, title: str, dir_path: str, doc_file: str, categories: List[str],
                 created_at: Optional[datetime], updated_at: Optional[datetime] = None):
        self.__id = docs_id
        self.__title = title
        self.__dir_path = dir_path
        self.__doc_file = doc_file
        self.__top_category = categories[0] if not len(categories) == 0 else NON_CATEGORY_GROUP_NAME
        self.__categories = categories
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
    def doc_file(self):
        return self.__doc_file

    @property
    def categories(self):
        return self.__categories

    @property
    def top_category(self) -> str:
        return self.__top_category

    @property
    def created_at(self):
        return convert_datetime_to_entry_time_str(self.__created_at)

    @property
    def updated_at(self):
        return convert_datetime_to_entry_time_str(self.__updated_at)

    @property
    def updated_at_month_day(self):
        return convert_datetime_to_month_day_str(self.__updated_at)

    def build_id_to_title(self) -> Dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.dir_path}{self.doc_file})'

    def build_dump_data(self, json_data=None) -> object:
        return {
            DocEntry.FIELD_ID: resolve_dump_field_data(self, json_data, DocEntry.FIELD_ID),
            DocEntry.FIELD_TITLE: resolve_dump_field_data(self, json_data, DocEntry.FIELD_TITLE),
            DocEntry.FIELD_DIR_PATH: resolve_dump_field_data(self, json_data, DocEntry.FIELD_DIR_PATH),
            DocEntry.FIELD_DOC_FILE: resolve_dump_field_data(self, json_data, DocEntry.FIELD_DOC_FILE),
            DocEntry.FIELD_TOP_CATEGORY: resolve_dump_field_data(self, json_data, DocEntry.FIELD_TOP_CATEGORY),
            DocEntry.FIELD_CATEGORIES: resolve_dump_field_data(self, json_data, DocEntry.FIELD_CATEGORIES),
            DocEntry.FIELD_CREATED_AT: resolve_dump_field_data(self, json_data, DocEntry.FIELD_CREATED_AT),
            DocEntry.FIELD_UPDATED_AT: resolve_dump_field_data(self, json_data, DocEntry.FIELD_UPDATED_AT),
        }

    def dump_data(self, dump_file_path: str):
        dump_entry_data(self, dump_file_path)

    @classmethod
    def init_from_dump_data(cls, dump_data: Dict[str, any]) -> DocEntry:
        return DocEntry(
            dump_data[DocEntry.FIELD_ID],
            dump_data[DocEntry.FIELD_TITLE],
            dump_data[DocEntry.FIELD_DIR_PATH],
            dump_data[DocEntry.FIELD_DOC_FILE],
            dump_data[DocEntry.FIELD_CATEGORIES],
            convert_entry_time_str_to_datetime(dump_data[DocEntry.FIELD_CREATED_AT]),
            convert_entry_time_str_to_datetime(dump_data[DocEntry.FIELD_UPDATED_AT])
        )

    @classmethod
    def deserialize_entry_data(cls, entry_id: str) -> DocEntry:
        dump_file_path = f'{LOCAL_DOCS_ENTRY_DUMP_DIR}{entry_id}.json'
        json_data = load_json(dump_file_path)
        return DocEntry.init_from_dump_data(json_data)


class DocEntries(IEntries):
    def __init__(self, entries: List[DocEntry] = None):
        self.__entries: List[DocEntry] = []
        if entries is not None:
            self.__entries: List[DocEntry] = entries

    @property
    def entry_list(self) -> List[DocEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def __add_entries(self, blog_entries: List[DocEntry]):
        self.__entries.extend(blog_entries)

    def merge(self, docs_entries: DocEntries):
        self.__add_entries(docs_entries.get_entries())

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    def dump_all_data(self, local_entry_list_file_path: str):
        # Todo: refactor
        json_data = load_json(local_entry_list_file_path)
        json_entries = {}
        if 'entries' in json_data:
            json_entries = json_data['entries']
        for entry in self.__entries:
            # if not entry.id in json_entries:
            # update file when the entry json file already exists.
            json_entries[entry.id] = entry.title
            entry.dump_data(f'{LOCAL_DOCS_ENTRY_DUMP_DIR}/{entry.id}.json')
        # dump data format
        # {
        #   "updated_time": "2022-01-02T03:04:05",
        #   "entries": {
        #     "id": "title"
        #      :
        #   }
        # }
        json_data['entries'] = json_entries
        dump_json(LOCAL_DOCS_ENTRY_LIST_PATH, json_data)

    def __add_entry(self, blog_entry: DocEntry):
        self.__entries.append(blog_entry)

    @classmethod
    def deserialize_grouping_data(cls, entry_id_to_title: Dict[str, str]) -> DocEntries:
        self = DocEntries()
        for entry_id in entry_id_to_title.keys():
            self.__add_entry(DocEntry.deserialize_entry_data(entry_id))
        return self
