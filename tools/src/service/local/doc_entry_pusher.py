from typing import List

from common.constant import BACKUP_DIR_PATH
from docs.docs_movers import resolve_move_from_and_move_to_dir_path_dict, move_documents_to_docs_dir
from domain.doc.doc_entry import new_doc_entries, DocEntries
from file.category_group_def import CategoryGroupDef
from file.files_operator import is_exist_dir, delete_dir
from service.local.doc_entry_index_updater import update_entry_grouping_and_index


def push_documents_to_docs(category_group_def: CategoryGroupDef, target_dir_names: List[str] = None) -> DocEntries:
    move_from_path_to_move_to_path_dict = resolve_move_from_and_move_to_dir_path_dict(category_group_def,
                                                                                      target_dir_names)
    # Todo: specifiable entry id
    # Todo: validate dir name
    docs_entries = new_doc_entries(move_from_path_to_move_to_path_dict)
    for entry in docs_entries.entry_list:
        # if exist backup, remove backup
        target_dir_path = f'{BACKUP_DIR_PATH}{entry.id}'
        if is_exist_dir(target_dir_path):
            delete_dir(target_dir_path)

    docs_entries.dump_all_data()
    # category_to_docs_entries = CategoryToEntriesMap(docs_entries)
    # group_to_categorized_docs_entries = GroupToCategorizedEntriesMap(category_group_def, category_to_docs_entries)
    # group_to_categorized_docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)

    update_entry_grouping_and_index(category_group_def, docs_entries)
    move_documents_to_docs_dir(move_from_path_to_move_to_path_dict)
    return docs_entries
