from typing import Dict

from common.constant import LOCAL_DOCS_ENTRY_GROUPING_PATH
from domain.doc.doc_entry import DocEntries, DocEntry
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import load_json


class DocsGroupingDataDeserializer:
    def __init__(self, dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                 category_group_def: CategoryGroupDef, grouping_json_path: str = None):
        self.dump_doc_data_accessor = dump_doc_data_accessor
        self.category_group_def = category_group_def
        self.grouping_json_path = grouping_json_path if grouping_json_path is not None else LOCAL_DOCS_ENTRY_GROUPING_PATH

    def execute(self) -> GroupToCategorizedEntriesMap:
        group_to_categorized_entries: Dict[str, Dict[str, Dict[str, str]]] = load_json(self.grouping_json_path)

        grouping_entries_map = GroupToCategorizedEntriesMap.deserialize_grouping_entries_data(
            self.dump_doc_data_accessor, self.category_group_def, group_to_categorized_entries)
        # print(grouping_entries_map.convert_md_lines())
        return grouping_entries_map
