from common.constant import LOCAL_DOCS_ENTRY_DUMP_DIR, LOCAL_DOCS_ENTRY_LIST_PATH
from domain.doc.doc_entry import DocEntries, DocEntry
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from dump.interface import IDumpEntriesAccessor


class DumpDocEntriesAccessor(IDumpEntriesAccessor[DocEntries, DocEntry]):
    def __init__(self):
        entry_accessor = DumpEntryAccessor[DocEntry](LOCAL_DOCS_ENTRY_DUMP_DIR)
        self.__entries_accessor: IDumpEntriesAccessor = \
            DumpEntriesAccessor[DocEntries](LOCAL_DOCS_ENTRY_LIST_PATH, entry_accessor)

    def load_entries(self) -> DocEntries:
        return self.__entries_accessor.load_entries()

    def save_entries(self, entries: DocEntries):
        return self.__entries_accessor.save_entries(entries)

    def load_entry(self, entry_id: str) -> DocEntry:
        return self.__entries_accessor.load_entry(entry_id)

    def save_entry(self, entry: DocEntry):
        return self.__entries_accessor.save_entry(entry)
