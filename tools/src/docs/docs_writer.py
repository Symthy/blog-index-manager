from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from domain.doc.doc_entry import DocEntries, DocEntry
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef


def save_doc_entries(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                     grouping_doc_entries_deserializer: DocsGroupingDataDeserializer, new_docs_entries: DocEntries):
    dump_doc_data_accessor.save_entries(new_docs_entries)
    grouping_doc_entries: GroupToCategorizedEntriesMap = grouping_doc_entries_deserializer.execute()
    grouping_doc_entries.add_entries(new_docs_entries)
    grouping_doc_entries.dump_docs_data()
