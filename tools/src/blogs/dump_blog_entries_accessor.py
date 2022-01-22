from typing import Optional, List

from common.constant import HATENA_BLOG_ENTRY_LIST_PATH, HATENA_BLOG_ENTRY_DUMP_DIR
from domain.blog.blog_entry import BlogEntries, BlogEntry
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from dump.interface import IDumpEntriesAccessor


class DumpBlogEntriesAccessor(IDumpEntriesAccessor[BlogEntries, BlogEntry]):
    def __init__(self):
        entry_accessor = DumpEntryAccessor[BlogEntry](HATENA_BLOG_ENTRY_DUMP_DIR)
        self.__entries_accessor: IDumpEntriesAccessor = \
            DumpEntriesAccessor[BlogEntries, BlogEntry](HATENA_BLOG_ENTRY_LIST_PATH, entry_accessor)

    def load_entries(self, target_entry_ids: Optional[List[str]] = None) -> BlogEntries:
        return self.__entries_accessor.load_entries(target_entry_ids)

    def save_entries(self, entries: BlogEntries):
        return self.__entries_accessor.save_entries(entries)

    def load_entry(self, target_entry_id: str) -> BlogEntry:
        return self.__entries_accessor.load_entry(target_entry_id)

    def save_entry(self, entry: BlogEntry):
        return self.__entries_accessor.save_entry(entry)
