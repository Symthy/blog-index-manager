from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from common.constant import NON_CATEGORY_GROUP_NAME, LOCAL_DOCS_ENTRY_LIST_PATH, CATEGORY_FILE_NAME, \
    LOCAL_DOCS_ENTRY_DUMP_DIR
from docs.document_register import get_doc_title_from_md_file
from domain.data_dumper import dump_entry_data, resolve_dump_field_data
from domain.interface import IEntry, IEntries
from file.file_accessor import load_json, dump_json, read_text_file
from file.files_operator import make_new_file, get_md_file_path_in_target_dir
from ltime.time_resolver import convert_datetime_to_month_day_str, convert_datetime_to_entry_time_str, \
    resolve_entry_current_time, get_current_time, convert_datetime_to_time_sequence


def new_doc_entries(move_from_path_to_move_to_path_dict: Dict[str, str]) -> DocEntries:
    docs_entry_list = []
    for move_from_path, move_to_path in move_from_path_to_move_to_path_dict.items():
        docs_entry_opt = new_doc_entry(move_from_path, move_to_path)
        if docs_entry_opt is not None:
            docs_entry_list.append(docs_entry_opt)
    return DocEntries(docs_entry_list)


def new_doc_entry(target_dir_path: str, move_to_path: str) -> Optional[DocEntry]:
    created_datetime: datetime = get_current_time()
    docs_id = convert_datetime_to_time_sequence(created_datetime)
    id_file = f'{target_dir_path}/.{docs_id}'
    md_file_path = get_md_file_path_in_target_dir(target_dir_path)
    dir_name = target_dir_path.rsplit('/', 1)[1]
    file_name = md_file_path.rsplit('/', 1)[1]
    if md_file_path is None:
        print(f'[Error] skip: non exist md file (dir: {dir_name})')
        return None
    doc_title = get_doc_title_from_md_file(md_file_path)
    if doc_title is None:
        print(f'[Error] skip: empty doc title (dir: {dir_name})')
        return None
    make_new_file(id_file)
    categories = read_text_file(target_dir_path + CATEGORY_FILE_NAME)
    return DocEntry(docs_id, doc_title, move_to_path, file_name, categories, created_datetime)


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
                 created_at: datetime = None, updated_at: Optional[datetime] = None):
        self.__id = docs_id
        self.__title = title
        self.__dir_path = dir_path
        self.__doc_file = doc_file
        self.__top_category = categories[0] if not len(categories) == 0 else NON_CATEGORY_GROUP_NAME
        self.__categories = categories
        self.__created_at: datetime = created_at
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
    def deserialize_grouping_data(cls, entry_id: str, title: str, category: str) -> DocEntry:
        return DocEntry(entry_id, title, '', '', [category], None, None)


class DocEntries(IEntries):
    def __init__(self, entries: List[DocEntry] = None):
        self.__entries: List[DocEntry] = []
        if entries is not None:
            self.__entries: List[DocEntry] = entries

    def get_entries(self) -> List[DocEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def __add_entries(self, blog_entries: List[DocEntry]):
        self.__entries.extend(blog_entries)

    def merge(self, docs_entries: DocEntries):
        self.__add_entries(docs_entries.get_entries())

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    def dump_all_data(self, dump_file_path: str):
        # Todo: refactor
        json_data = load_json(dump_file_path)
        json_data['updated_time'] = resolve_entry_current_time()
        json_entries = {}
        if 'entries' in json_data:
            json_entries = json_data['entries']
        for entry in self.__entries:
            if not entry.id in json_entries:
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
    def deserialize_grouping_data(cls, category: str, entry_id_to_title: Dict[str, str]) -> DocEntries:
        self = DocEntries()
        for entry_id, title in entry_id_to_title.items():
            self.__add_entry(DocEntry.deserialize_grouping_data(entry_id, title, category))
        return self
