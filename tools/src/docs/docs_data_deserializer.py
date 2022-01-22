from typing import Optional

from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IEntries
from files.category_group_def import CategoryGroupDef


def deserialize_doc_entry_grouping_data(category_group_def: CategoryGroupDef,
                                        add_docs_entries: Optional[IEntries] = None) -> GroupToCategorizedEntriesMap:
    entry_index_result_map = GroupToCategorizedEntriesMap.deserialize_docs_grouping_data(category_group_def)
    if add_docs_entries is not None:
        entry_index_result_map.add_entries(category_group_def, add_docs_entries)
    return entry_index_result_map
