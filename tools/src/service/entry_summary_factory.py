from typing import List

from blogs.blog_grouping_deserializer import deserialize_grouping_blog_entries
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.doc.doc_entry import DocEntries, DocEntry
from domain.entry_summary import EntrySummary
from dump.blog_to_doc_mapping import BlogDocEntryMapping
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef


# Todo: split blog and doc
class EntrySummaryFactory:
    def __init__(self, dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                 dump_blog_data_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
                 category_group_def: CategoryGroupDef, grouping_doc_entries_deserializer: DocsGroupingDataDeserializer):
        self.__blog_doc_mapping = BlogDocEntryMapping()
        self.__dump_doc_data_accessor = dump_doc_data_accessor
        self.__dump_blog_data_accessor = dump_blog_data_accessor
        self.__category_group_def = category_group_def
        self.__grouping_doc_entries_deserializer = grouping_doc_entries_deserializer

    def resolve_pickup_doc_entries(self):
        all_doc_entries: DocEntries = self.__dump_doc_data_accessor.load_entries()
        pickup_doc_entries = all_doc_entries.get_pickup_entries()
        return DocEntries(pickup_doc_entries)

    def resolve_pickup_blog_entries(self):
        pickup_doc_entries: DocEntries = self.resolve_pickup_doc_entries()
        blog_entry_ids: List[str] = self.__blog_doc_mapping.get_blog_entry_ids(
            [entry.id for entry in pickup_doc_entries.entry_list])
        blog_entries: BlogEntries = self.__dump_blog_data_accessor.load_entries(blog_entry_ids)
        return blog_entries

    def build_doc_entry_summary(self):
        grouping_entries_map = self.__grouping_doc_entries_deserializer.execute()
        EntrySummary(self.resolve_pickup_doc_entries(), grouping_entries_map)

    def build_blog_entry_summary(self):
        grouping_entries_map = deserialize_grouping_blog_entries(self.__dump_blog_data_accessor,
                                                                 self.__category_group_def)
        return EntrySummary(self.resolve_pickup_blog_entries(), grouping_entries_map)
