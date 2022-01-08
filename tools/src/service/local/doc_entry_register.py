from typing import List

from common.constant import LOCAL_DOCS_ENTRY_LIST_PATH, LOCAL_DOCS_ENTRY_GROUPING_PATH
from docs.document_register import resolve_move_from_and_move_to_dir_path_dict
from domain.category_to_entries import CategoryToEntriesMap
from domain.doc_entry import new_doc_entries
from domain.group_to_categories import GroupToCategorizedEntriesMap
from file.category_group_def import CategoryGroupDef
from file.file_accessor import load_json


def push_documents_to_docs(category_group_def: CategoryGroupDef, target_dir_names: List[str] = None):
    move_from_path_to_move_to_path_dict = resolve_move_from_and_move_to_dir_path_dict(category_group_def,
                                                                                      target_dir_names)
    docs_entries = new_doc_entries(move_from_path_to_move_to_path_dict)
    docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_LIST_PATH)
    category_to_docs_entries = CategoryToEntriesMap(docs_entries)
    group_to_categorized_docs_entries = GroupToCategorizedEntriesMap(category_group_def, category_to_docs_entries)
    group_to_categorized_docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)

    json_data = load_json(LOCAL_DOCS_ENTRY_GROUPING_PATH)
    dump_data = GroupToCategorizedEntriesMap.deserialize_docs_grouping_data(category_group_def, json_data)
    print(dump_data.convert_md_lines())
    # dump_data.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)
    # move_documents_to_docs_dir(move_from_path_to_move_to_path_dict)
