from typing import List

from docs.docs_movers import resolve_move_from_and_move_to_dir_path_dict
from domain.doc_entry import new_doc_entries, DocEntries
from file.category_group_def import CategoryGroupDef
from service.local.doc_entry_index_updater import update_entry_grouping_and_index


def push_documents_to_docs(category_group_def: CategoryGroupDef, target_dir_names: List[str] = None) -> DocEntries:
    move_from_path_to_move_to_path_dict = resolve_move_from_and_move_to_dir_path_dict(category_group_def,
                                                                                      target_dir_names)
    docs_entries = new_doc_entries(move_from_path_to_move_to_path_dict)
    docs_entries.dump_all_data()
    # category_to_docs_entries = CategoryToEntriesMap(docs_entries)
    # group_to_categorized_docs_entries = GroupToCategorizedEntriesMap(category_group_def, category_to_docs_entries)
    # group_to_categorized_docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)

    update_entry_grouping_and_index(category_group_def, docs_entries)
    # move_documents_to_docs_dir(move_from_path_to_move_to_path_dict)
    return docs_entries
