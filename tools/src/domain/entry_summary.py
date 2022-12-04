from typing import List

from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IEntries

PICKUP_ENTRY_HEAD_LINE = 'Pickup:'
ALL_ENTRY_HEAD_LINE = 'All:'


class EntrySummary:
    def __init__(self, pickup_entries: IEntries, entries_grouping_map: GroupToCategorizedEntriesMap):
        self.__pickup_entries = pickup_entries
        self.__entries_grouping_map = entries_grouping_map

    @property
    def pickup_entry_lines(self) -> List[str]:
        return self.__pickup_entries.convert_md_lines()

    @property
    def all_entry_lines(self) -> List[str]:
        return self.__entries_grouping_map.convert_md_lines()

    @property
    def pickup_and_all_entry_lines(self) -> List[str]:
        lines: List[str] = [PICKUP_ENTRY_HEAD_LINE]
        lines.extend(self.pickup_entry_lines)
        lines.append('')
        lines.append(ALL_ENTRY_HEAD_LINE)
        lines.extend(self.all_entry_lines)
        return lines
