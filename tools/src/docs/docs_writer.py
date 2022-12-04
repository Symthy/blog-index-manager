from docs.docs_grouping_deserializer import deserialize_grouping_doc_entries
from domain.doc.doc_entry import DocEntries, DocEntry
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef


def save_doc_entries(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                     category_group_def: CategoryGroupDef, new_docs_entries: DocEntries):
    dump_doc_data_accessor.save_entries(new_docs_entries)
    grouping_doc_entries = deserialize_grouping_doc_entries(dump_doc_data_accessor, category_group_def)
    grouping_doc_entries.add_entries(category_group_def, new_docs_entries)
    grouping_doc_entries.dump_docs_data()
