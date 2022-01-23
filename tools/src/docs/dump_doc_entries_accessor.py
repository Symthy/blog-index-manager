from typing import Optional, List

from common.constant import LOCAL_DOCS_ENTRY_DUMP_DIR, LOCAL_DOCS_ENTRY_LIST_PATH
from domain.doc.doc_entry import DocEntries, DocEntry
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from dump.interface import IDumpEntriesAccessor


class DumpDocEntriesAccessor(IDumpEntriesAccessor[DocEntries, DocEntry]):
    def __init__(self):
        entry_accessor = DumpEntryAccessor[DocEntry](LOCAL_DOCS_ENTRY_DUMP_DIR)
        self.__entries_accessor: IDumpEntriesAccessor = \
            DumpEntriesAccessor[DocEntries, DocEntry](LOCAL_DOCS_ENTRY_LIST_PATH, entry_accessor)

    def load_entries(self, target_entry_ids: Optional[List[str]] = None) -> DocEntries:
        return self.__entries_accessor.load_entries(target_entry_ids)

    def save_entries(self, entries: DocEntries):
        return self.__entries_accessor.save_entries(entries)

    def load_entry(self, target_entry_id: str) -> DocEntry:
        return self.__entries_accessor.load_entry(target_entry_id)

    def save_entry(self, entry: DocEntry):
        return self.__entries_accessor.save_entry(entry)

    def search_entry_id(self, keyword: str) -> List[str]:
        return self.__entries_accessor.search_entry_id(keyword)

    def has_entry(self, entry_id: str) -> bool:
        return self.__entries_accessor.has_entry(entry_id)
