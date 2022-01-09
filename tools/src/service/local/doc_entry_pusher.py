from typing import List

from common.constant import LOCAL_DOCS_ENTRY_LIST_PATH, LOCAL_DOCS_ENTRY_GROUPING_PATH, \
    LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH
from docs.docs_data_deserializer import deserialize_doc_entry_grouping_data
from docs.docs_movers import resolve_move_from_and_move_to_dir_path_dict
from domain.doc_entry import new_doc_entries, DocEntries
from file.category_group_def import CategoryGroupDef
from file.file_accessor import write_text_lines


def push_documents_to_docs(category_group_def: CategoryGroupDef, target_dir_names: List[str] = None) -> DocEntries:
    move_from_path_to_move_to_path_dict = resolve_move_from_and_move_to_dir_path_dict(category_group_def,
                                                                                      target_dir_names)
    docs_entries = new_doc_entries(move_from_path_to_move_to_path_dict)
    docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_LIST_PATH)
    # category_to_docs_entries = CategoryToEntriesMap(docs_entries)
    # group_to_categorized_docs_entries = GroupToCategorizedEntriesMap(category_group_def, category_to_docs_entries)
    # group_to_categorized_docs_entries.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)

    entry_index_result_map = deserialize_doc_entry_grouping_data(category_group_def, docs_entries)
    entry_index_result_map.dump_all_data(LOCAL_DOCS_ENTRY_GROUPING_PATH)
    write_text_lines(LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH, entry_index_result_map.convert_md_lines())
    # move_documents_to_docs_dir(move_from_path_to_move_to_path_dict)
    return docs_entries
