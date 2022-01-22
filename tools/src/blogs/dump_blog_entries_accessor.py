from common.constant import HATENA_BLOG_ENTRY_LIST_PATH, HATENA_BLOG_ENTRY_DUMP_DIR
from domain.blog.blog_entry import BlogEntries, BlogEntry
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from dump.interface import IDumpEntriesAccessor


class DumpBlogEntriesAccessor(IDumpEntriesAccessor[BlogEntries]):
    def __init__(self):
        entry_accessor = DumpEntryAccessor[BlogEntry](HATENA_BLOG_ENTRY_DUMP_DIR)
        self.__entries_accessor: IDumpEntriesAccessor = \
            DumpEntriesAccessor[BlogEntries](HATENA_BLOG_ENTRY_LIST_PATH, entry_accessor)

    def load_entries(self) -> BlogEntries:
        return self.__entries_accessor.load_entries()

    def save_entries(self, entries: BlogEntries):
        return self.__entries_accessor.save_entries(entries)
