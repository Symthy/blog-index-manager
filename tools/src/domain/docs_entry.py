from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from common.constant import NON_CATEGORY_NAME, LOCAL_DOCS_ENTRY_LIST_PATH, CATEGORY_FILE_NAME, LOCAL_DOCS_ENTRY_DUMP_DIR
from docs.document_register import get_doc_title_from_md_file
from domain.data_dumper import dump_entry_data, resolve_dump_field_data
from domain.interface import IEntry, IEntries
from file.file_accessor import load_json, dump_json, read_text_file
from file.files_operator import make_new_file, get_md_file_path_in_target_dir
from ltime.time_resolver import convert_datetime_to_month_day_str, convert_datetime_to_entry_time_str, \
    resolve_entry_current_time, get_current_time, convert_datetime_to_time_sequence


def new_docs_entries(move_from_path_to_move_to_path_dict: Dict[str, str]) -> DocsEntries:
    docs_entry_list = []
    for move_from_path, move_to_path in move_from_path_to_move_to_path_dict.items():
        docs_entry_opt = new_docs_entry(move_from_path, move_to_path)
        if docs_entry_opt is not None:
            docs_entry_list.append(docs_entry_opt)
    return DocsEntries(docs_entry_list)


def new_docs_entry(target_dir_path: str, move_to_path: str) -> Optional[DocsEntry]:
    created_datetime: datetime = get_current_time()
    docs_id = convert_datetime_to_time_sequence(created_datetime)
    id_file = f'{target_dir_path}/.{docs_id}'
    md_file_path = get_md_file_path_in_target_dir(target_dir_path)
    dir_name = target_dir_path.rsplit('/', 1)[1]
    if md_file_path is None:
        print(f'[Error] skip: non exist md file (dir: {dir_name})')
        return None
    doc_title = get_doc_title_from_md_file(md_file_path)
    if doc_title is None:
        print(f'[Error] skip: empty doc title (dir: {dir_name})')
        return None
    make_new_file(id_file)
    categories = read_text_file(target_dir_path + CATEGORY_FILE_NAME)
    return DocsEntry(docs_id, doc_title, move_to_path, categories, created_datetime)


class DocsEntry(IEntry):
    def __init__(self, docs_id: str, title: str, dir_path: str, categories: List[str], created_at: datetime,
                 updated_at: Optional[datetime] = None):
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
        return convert_datetime_to_entry_time_str(self.__created_at)

    @property
    def updated_at(self):
        return convert_datetime_to_entry_time_str(self.__updated_at)

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
