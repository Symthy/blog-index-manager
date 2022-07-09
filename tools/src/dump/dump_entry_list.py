from __future__ import annotations

from typing import Dict, List, Any, Generic, Optional

from dump.dump_entry_accessor import DumpEntryAccessor
from dump.interface import TS, TM
from files.file_accessor import load_json
from ltime.time_resolver import resolve_entry_current_time


class DumpEntryList(Generic[TM, TS]):
    """
    xxx_entry_list.jsonの全データを保持するクラス
    """
    FIELD_UPDATED_TIME = 'updated_time'
    FIELD_ENTRIES = 'entries'

    def __init__(self, entry_list_file_path: str, dump_entry_accessor: DumpEntryAccessor[TS]):
        self.__dump_entry_accessor = dump_entry_accessor
        dump_data = load_json(entry_list_file_path)
        self.__updated_time: str = dump_data[DumpEntryList.FIELD_UPDATED_TIME] \
            if DumpEntryList.FIELD_UPDATED_TIME in dump_data else resolve_entry_current_time()
        self.__entry_id_to_title: Dict[str, str] = dump_data[DumpEntryList.FIELD_ENTRIES] \
            if DumpEntryList.FIELD_ENTRIES in dump_data else {}

    @property
    def entry_ids(self) -> List[str]:
        return list(self.__entry_id_to_title.keys())

    def push_entry(self, entry: TS):
        self.__entry_id_to_title[entry.id] = entry.title

    def search_by_title(self, keyword: str) -> List[str]:
        entry_ids = [eid for eid, title in self.__entry_id_to_title.items() if keyword.lower() in title.lower()]
        return entry_ids

    def build_dump_data(self) -> Dict[str, Any]:
        return {
            DumpEntryList.FIELD_UPDATED_TIME: resolve_entry_current_time(),
            DumpEntryList.FIELD_ENTRIES: self.__entry_id_to_title
        }

    def convert_entries(self, target_entry_ids: Optional[List[str]] = None) -> List[TS]:
        if target_entry_ids is None:
            entry_list: List[TS] = [self.__dump_entry_accessor.load_entry(entry_id) for entry_id in self.entry_ids]
        else:
            # filter target entry ids
            entry_list: List[TS] = [self.__dump_entry_accessor.load_entry(entry_id) for entry_id in self.entry_ids
                                    if entry_id in target_entry_ids]
        return entry_list

# dump data format
# {
#   "updated_time": "2022-01-02T03:04:05",
#   "entries": {
#     "id": "title"
#      :
#   }
# }
