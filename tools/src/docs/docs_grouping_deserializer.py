from typing import Optional

from docs.dump_doc_entries_accessor import DumpDocEntriesAccessor
from domain.doc.doc_entry import DocEntries
from domain.group_to_categories import GroupToCategorizedEntriesMap
from files.conf.category_group_def import CategoryGroupDef


def deserialize_doc_entry_grouping_data(category_group_def: CategoryGroupDef,
                                        add_docs_entries: Optional[DocEntries] = None) -> GroupToCategorizedEntriesMap:
    entry_grouping_map = GroupToCategorizedEntriesMap.deserialize_entry_grouping_data(DumpDocEntriesAccessor(),
                                                                                      category_group_def)
    # print(entry_grouping_map.convert_md_lines())
    if add_docs_entries is not None:
        entry_grouping_map.add_entries(category_group_def, add_docs_entries)
    return entry_grouping_map
