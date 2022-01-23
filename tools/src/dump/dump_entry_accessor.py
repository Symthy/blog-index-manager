from collections import Callable
from typing import Dict, Any, Optional

from common.constant import LOCAL_DOCS_ENTRY_DUMP_DIR, HATENA_BLOG_ENTRY_DUMP_DIR
from domain.blog.blog_entry import BlogEntry
from domain.doc.doc_entry import DocEntry
from dump.entry_data_dumper import dump_entry_data
from dump.interface import TS, IDumpEntryAccessor
from files.file_accessor import load_json


class DumpEntryAccessor(IDumpEntryAccessor[TS]):
    __DUMP_DIR_TO_ENTRY_FACTORY: Dict[str, Callable[[dict[str, Any]], TS]] = {
        HATENA_BLOG_ENTRY_DUMP_DIR: BlogEntry.init_from_dump_data,
        LOCAL_DOCS_ENTRY_DUMP_DIR: DocEntry.init_from_dump_data
    }

    def __init__(self, dump_dir_path, entry_factory: Optional[Callable] = None):
        self.__entry_dump_dir_path = dump_dir_path
        self.__entry_factory = DumpEntryAccessor.__DUMP_DIR_TO_ENTRY_FACTORY[dump_dir_path] \
            if entry_factory is None else entry_factory

    def load_entry(self, entry_id: str) -> TS:
        dump_file_path = f'{self.__entry_dump_dir_path}{entry_id}.json'
        json_data = load_json(dump_file_path)
        return self.__entry_factory(json_data)

    def save_entry(self, entry: TS):
        dump_entry_data(entry, f'{self.__entry_dump_dir_path}{entry.id}.json')
