from typing import Optional, Callable, Dict, Any, List

from common.constant import LOCAL_DOCS_ENTRY_LIST_PATH, \
    HATENA_BLOG_ENTRY_LIST_PATH
from domain.blog.blog_entry import BlogEntries
from domain.doc.doc_entry import DocEntries
from dump.dump_entry_accessor import DumpEntryAccessor
from dump.dump_entry_list import DumpEntryList
from dump.interface import IDumpEntriesAccessor, TM, TS
from files.file_accessor import dump_json


class DumpEntriesAccessor(IDumpEntriesAccessor[TM, TS]):
    __DUMP_FILE_TO_ENTRIES_FACTORY: Dict[str, Callable[[Optional[List[TS]]], TM]] = {
        HATENA_BLOG_ENTRY_LIST_PATH: BlogEntries.new_instance,
        LOCAL_DOCS_ENTRY_LIST_PATH: DocEntries.new_instance
    }

    def __init__(self, entry_list_file_path: str, dump_entry_accessor: DumpEntryAccessor[TS],
                 entries_factory: Optional[Callable[[Any], TM]] = None):
        self.__entry_list_file_path = entry_list_file_path
        self.__dump_entry_accessor = dump_entry_accessor
        self.__dump_entry_list = DumpEntryList(entry_list_file_path, dump_entry_accessor)
        self.__entries_factory = DumpEntriesAccessor.__DUMP_FILE_TO_ENTRIES_FACTORY[entry_list_file_path] \
            if entries_factory is None else entries_factory

    def load_entries(self, target_entry_ids: Optional[List[str]] = None) -> TM:
        entries = self.__entries_factory(self.__dump_entry_list.convert_entries(target_entry_ids))
        return entries

    def save_entries(self, entries: TM):
        for entry in entries.entry_list:
            self.__dump_entry_list.push_entry(entry)
            self.__dump_entry_accessor.save_entry(entry)
        dump_json(self.__entry_list_file_path, self.__dump_entry_list.build_dump_data())

    def load_entry(self, entry_id: str) -> TS:
        return self.__dump_entry_accessor.load_entry(entry_id)

    def save_entry(self, entry: TS):
        self.__dump_entry_accessor.save_entry(entry)

    def search_entry_id(self, keyword: str) -> List[str]:
        # Todo: specify other than title in keyword
        return self.__dump_entry_list.search_by_title(keyword)

    def has_entry(self, entry_id) -> bool:
        return entry_id in self.__dump_entry_list.entry_ids
