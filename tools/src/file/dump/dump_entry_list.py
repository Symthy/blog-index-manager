from __future__ import annotations

from typing import Dict, List

from common.constant import HATENA_BLOG_ENTRY_LIST_PATH, LOCAL_DOCS_ENTRY_LIST_PATH
from domain.interface import IEntry
from file.file_accessor import load_json, dump_json
from ltime.time_resolver import resolve_entry_current_time


class DumpEntryList:
    FIELD_UPDATED_TIME = 'updated_time'
    FIELD_ENTRIES = 'entries'

    def __init__(self, file_path: str):
        self.__dump_file_path = file_path
        dump_data = load_json(file_path)
        self.__updated_time: str = dump_data[DumpEntryList.FIELD_UPDATED_TIME] \
            if DumpEntryList.FIELD_UPDATED_TIME in dump_data else resolve_entry_current_time()
        self.__entry_id_to_title: Dict[str, str] = dump_data[DumpEntryList.FIELD_ENTRIES] \
            if DumpEntryList.FIELD_ENTRIES in dump_data else {}

    @classmethod
    def init_blog_entry_list(cls) -> DumpEntryList:
        return DumpEntryList(HATENA_BLOG_ENTRY_LIST_PATH)

    @classmethod
    def init_doc_entry_list(cls) -> DumpEntryList:
        return DumpEntryList(LOCAL_DOCS_ENTRY_LIST_PATH)

    @property
    def entry_ids(self) -> List[str]:
        return list(self.__entry_id_to_title.keys())

    def push_entry(self, entry: IEntry):
        self.__entry_id_to_title[entry.id] = entry.title

    def dump_file(self):
        dump_data = {
            DumpEntryList.FIELD_UPDATED_TIME: resolve_entry_current_time(),
            DumpEntryList.FIELD_ENTRIES: self.__entry_id_to_title
        }
        dump_json(self.__dump_file_path, dump_data)

# dump data format
# {
#   "updated_time": "2022-01-02T03:04:05",
#   "entries": {
#     "id": "title"
#      :
#   }
# }
