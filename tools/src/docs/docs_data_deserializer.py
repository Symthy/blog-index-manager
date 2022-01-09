from typing import Optional

from common.constant import LOCAL_DOCS_ENTRY_GROUPING_PATH
from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IEntries
from file.category_group_def import CategoryGroupDef
from file.file_accessor import load_json


def deserialize_doc_entry_grouping_data(category_group_def: CategoryGroupDef,
                                        add_docs_entries: Optional[IEntries] = None) -> GroupToCategorizedEntriesMap:
    json_data = load_json(LOCAL_DOCS_ENTRY_GROUPING_PATH)
    entry_index_result_map = GroupToCategorizedEntriesMap.deserialize_docs_grouping_data(category_group_def, json_data)
    if add_docs_entries is not None:
        entry_index_result_map.add_entries(category_group_def, add_docs_entries)
    return entry_index_result_map
