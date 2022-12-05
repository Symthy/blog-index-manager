from typing import List

from docs.docs_backuper import sava_backup_doc_entry, retrieve_backup_doc_entry
from docs.docs_grouping_deserializer import deserialize_grouping_doc_entries
from domain.doc.doc_entry import DocEntry, DocEntries
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef


def retrieve_document_from_docs(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                                category_group_def: CategoryGroupDef, entry_ids: List[str]):
    grouping_doc_entries: GroupToCategorizedEntriesMap = deserialize_grouping_doc_entries(
        dump_doc_data_accessor, category_group_def)
    for doc_entry_id in entry_ids:
        if not dump_doc_data_accessor.has_entry(doc_entry_id):
            print(f'[Error] Nothing specified document (id: {doc_entry_id})')
            return
        target_doc_entry = dump_doc_data_accessor.load_entry(doc_entry_id)
        sava_backup_doc_entry(target_doc_entry)
        grouping_doc_entries.remove_entry(category_group_def, target_doc_entry)
    grouping_doc_entries.dump_docs_data()


def cancel_retrieving_document(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                               category_group_def: CategoryGroupDef, entry_ids: List[str]):
    group_to_categorized_entries: GroupToCategorizedEntriesMap = deserialize_grouping_doc_entries(
        dump_doc_data_accessor, category_group_def)
    for doc_entry_id in entry_ids:
        retrieve_backup_doc_entry(doc_entry_id)
        doc_entry = dump_doc_data_accessor.load_entry(doc_entry_id)
        group_to_categorized_entries.add_entry(category_group_def, doc_entry)
    group_to_categorized_entries.dump_docs_data()
