from typing import List, Optional

from common.constant import BACKUP_DIR_PATH
from docs.docs_movers import resolve_move_from_and_move_to_dir_path_dict, move_documents_to_docs_dir
from domain.doc.doc_entry import new_doc_entries, DocEntries, DocEntry
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.files_operator import is_exist_dir, delete_dir
from service.local.doc_entry_index_updater import update_entry_grouping_and_summary


def push_documents_to_docs(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                           category_group_def: CategoryGroupDef,
                           target_dir_names: List[str] = None) -> Optional[DocEntries]:
    move_from_path_to_move_to_path_dict = resolve_move_from_and_move_to_dir_path_dict(category_group_def,
                                                                                      target_dir_names)
    if len(move_from_path_to_move_to_path_dict) == 0:
        return None
    # Todo: specifiable entry id
    # Todo: validate dir name
    new_docs_entries = new_doc_entries(move_from_path_to_move_to_path_dict)
    for entry in new_docs_entries.entry_list:
        # if exist backup, remove backup
        target_dir_path = f'{BACKUP_DIR_PATH}{entry.id}'
        if is_exist_dir(target_dir_path):
            delete_dir(target_dir_path)

    dump_doc_data_accessor.save_entries(new_docs_entries)
    # category_to_docs_entries = CategoryToEntriesMap(docs_entries)
    # group_to_categorized_docs_entries = GroupToCategorizedEntriesMap(category_group_def, category_to_docs_entries)
    # group_to_categorized_docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)

    update_entry_grouping_and_summary(category_group_def, new_docs_entries)
    move_documents_to_docs_dir(move_from_path_to_move_to_path_dict)
    return new_docs_entries
