from typing import List, Optional

from docs.docs_backuper import DocsBackuper
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from docs.docs_mover import move_documents_to_docs_dir, DocsMover
from domain.doc.doc_entry import DocEntries, DocEntry
from domain.doc.doc_entry_factory import build_doc_entries
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from service.local.doc_entry_summary_writer import DocEntrySummaryWriter


class DocEntryPusher:
    def __init__(self, dump_doc_data_accessor, category_group_def, doc_entry_summary_writer, docs_backuper, docs_mover,
                 grouping_doc_entries_deserializer):
        self.__dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry] = dump_doc_data_accessor
        self.__category_group_def: CategoryGroupDef = category_group_def
        self.__doc_entry_summary_writer: DocEntrySummaryWriter = doc_entry_summary_writer
        self.__docs_backuper: DocsBackuper = docs_backuper
        self.__docs_mover: DocsMover = docs_mover
        self.__grouping_doc_entries_deserializer: DocsGroupingDataDeserializer = grouping_doc_entries_deserializer

    def execute(self, is_pickup: bool, target_dir_names: List[str] = None) -> Optional[DocEntries]:
        moving_from_and_to_path_dict = self.__docs_mover.resolve_moving_from_and_to_dir_path(target_dir_names)
        if len(moving_from_and_to_path_dict) == 0:
            return None
        # Todo: specifiable entry id
        # Todo: validate dir name
        new_doc_entries = build_doc_entries(self.__dump_doc_data_accessor, moving_from_and_to_path_dict, is_pickup)
        self.__docs_backuper.remove_backup_doc_entries(new_doc_entries)

        self.__save_doc_entries(new_doc_entries)
        self.__doc_entry_summary_writer.update_file()
        move_documents_to_docs_dir(moving_from_and_to_path_dict)
        return new_doc_entries

    def __save_doc_entries(self, new_docs_entries: DocEntries):
        self.__dump_doc_data_accessor.save_entries(new_docs_entries)
        grouping_doc_entries: GroupToCategorizedEntriesMap = self.__grouping_doc_entries_deserializer.execute()
        grouping_doc_entries.add_entries(new_docs_entries)
        grouping_doc_entries.dump_docs_data()
