from typing import List

from docs.docs_backuper import DocsBackuper
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from domain.doc.doc_entry import DocEntry, DocEntries
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor


class DocEntryRetriever:

    def __init__(self, dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                 docs_backuper: DocsBackuper, grouping_doc_entries_deserializer: DocsGroupingDataDeserializer):
        self.__dump_doc_data_accessor = dump_doc_data_accessor
        self.__docs_backuper = docs_backuper
        self.__grouping_doc_entries_deserializer = grouping_doc_entries_deserializer

    def retrieve_document_from_docs(self, entry_ids: List[str]):
        grouping_doc_entries: GroupToCategorizedEntriesMap = self.__grouping_doc_entries_deserializer.execute()
        for doc_entry_id in entry_ids:
            if not self.__dump_doc_data_accessor.has_entry(doc_entry_id):
                print(f'[Error] Nothing specified document (id: {doc_entry_id})')
                return
            target_doc_entry = self.__dump_doc_data_accessor.load_entry(doc_entry_id)
            self.__docs_backuper.sava_backup_doc_entry(target_doc_entry)
            grouping_doc_entries.remove_entry(target_doc_entry)
        grouping_doc_entries.dump_docs_data()

    def cancel_retrieving_document(self, entry_ids: List[str]):
        group_to_categorized_entries: GroupToCategorizedEntriesMap = self.__grouping_doc_entries_deserializer.execute()
        for doc_entry_id in entry_ids:
            self.__docs_backuper.retrieve_backup_doc_entry(doc_entry_id)
            doc_entry = self.__dump_doc_data_accessor.load_entry(doc_entry_id)
            group_to_categorized_entries.add_entry(doc_entry)
        group_to_categorized_entries.dump_docs_data()
