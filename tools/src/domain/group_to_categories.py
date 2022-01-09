from __future__ import annotations

from functools import reduce
from typing import List, Dict, Optional

from domain.category_to_entries import CategoryToEntriesMap, CategoryToEntriesSet, NON_CATEGORY_GROUP_NAME
from domain.interface import IConvertibleMarkdownLines, IEntry, IEntries
from file.category_group_def import CategoryGroupDef
from file.file_accessor import dump_json

DUMP_NON_CATEGORY_KEY = '-'


class GroupToCategorizedEntriesSet(IConvertibleMarkdownLines):
    def __init__(self, group: str):
        self.__group = group
        self.__categories = []
        self.__category_to_entries: Dict[str, CategoryToEntriesSet] = {}  # key: category
        self.__entries_of_non_category: Dict[str, IEntry] = {}  # key: entry_id

    @property
    def categories(self):
        return self.__categories

    @property
    def category_to_entries_list(self) -> List[CategoryToEntriesSet]:
        return list(self.__category_to_entries.values())

    @property
    def entry_list_of_non_category(self) -> List[IEntry]:
        return list(self.__entries_of_non_category.values())

    def __has_category(self, category: str) -> bool:
        return category in self.__categories

    def get_entries(self, category: Optional[str] = None) -> List[IEntry]:
        if category is None:
            # return all
            inner_entries_list: List[List[IEntry]] = list(
                map(lambda cte: cte.entry_list, self.category_to_entries_list))
            return reduce(lambda base, entry: base + entry, inner_entries_list)
        if self.__has_category(category):
            category_to_entries = self.__category_to_entries[category]
            return category_to_entries.entry_list
        return []

    def add_category_to_entries_set(self, category_to_entries: CategoryToEntriesSet):
        if category_to_entries.is_empty():
            return
        self.__categories.append(category_to_entries.category)
        self.__category_to_entries[category_to_entries.category] = category_to_entries

    def __add_category_to_entries_set_list(self, category_to_entries_set_list: List[CategoryToEntriesSet]):
        for category_to_entries_set in category_to_entries_set_list:
            self.add_category_to_entries_set(category_to_entries_set)

    def __add_entry_to_non_category(self, entry: IEntry):
        self.__entries_of_non_category[entry.id] = entry

    def add_entries_to_non_category(self, entries: List[IEntry]):
        for entry in entries:
            self.__entries_of_non_category[entry.id] = entry

    def __add_category(self, category: str):
        self.__categories.append(category)
        self.__categories.sort()

    def add_entry(self, entry: IEntry):
        # if entry.top_category is None or len(entry.top_category) == 0:
        if entry.top_category == NON_CATEGORY_GROUP_NAME:
            self.__add_entry_to_non_category(entry)
            return
        if entry.top_category in self.__categories:
            category_to_entries_set = self.__category_to_entries[entry.top_category]
            category_to_entries_set.add_entry(entry)
        else:
            self.__add_category(entry.top_category)
            self.__category_to_entries[entry.top_category] = CategoryToEntriesSet(entry.top_category, entry)

    def is_empty(self) -> bool:
        return len(self.__category_to_entries) == 0 and len(self.__entries_of_non_category) == 0

    def convert_md_lines(self) -> List[str]:
        lines: List[str] = [f'- {self.__group}']
        for category_to_entries in self.category_to_entries_list:
            category_to_entries_lines = list(map(lambda line: '  ' + line, category_to_entries.convert_md_lines()))
            lines = lines + category_to_entries_lines
        for entry in self.entry_list_of_non_category:
            lines.append('  ' + entry.convert_md_line())
        return lines

    @classmethod
    def __init_from_dump_data(cls, group: str,
                              category_to_entries_map: CategoryToEntriesMap) -> GroupToCategorizedEntriesSet:
        self = GroupToCategorizedEntriesSet(group)
        non_category_to_entries: Optional[CategoryToEntriesSet] = category_to_entries_map.pop(DUMP_NON_CATEGORY_KEY)
        self.__add_category_to_entries_set_list(category_to_entries_map.category_to_entries_sets)
        if non_category_to_entries is not None:
            for entry in non_category_to_entries.entry_list:
                self.__entries_of_non_category[entry.id] = entry
        return self

    @classmethod
    def deserialize_docs_grouping_data(cls, group: str,
                                       category_to_entries_map: CategoryToEntriesMap) -> GroupToCategorizedEntriesSet:
        return GroupToCategorizedEntriesSet.__init_from_dump_data(group, category_to_entries_map)


class GroupToCategorizedEntriesMap(IConvertibleMarkdownLines):
    def __init__(self, category_group_def: CategoryGroupDef, category_to_entries_map: CategoryToEntriesMap = None):
        self.__sorted_groups: List[str] = []
        self.__group_to_categorized_entries: Dict[str, GroupToCategorizedEntriesSet] = {}  # key: group
        # initialize process
        if category_to_entries_map is not None:
            self.__init_based_category_group_def(category_group_def, category_to_entries_map)
            # Categories that don't exist in definitions are pushed under "Others"
            self.__init_non_exist_category_in_definition(category_group_def, category_to_entries_map)

    def __init_based_category_group_def(self, category_group_def: CategoryGroupDef,
                                        category_to_entries_map: CategoryToEntriesMap):
        for grouping_categories in category_group_def.grouping_categories:
            def_group = grouping_categories.group_name
            def_categories = grouping_categories.categories
            self.__sorted_groups.append(def_group)  # the order of groups follows the definition(category_group.yml)
            if category_to_entries_map.is_exist_category(def_group):
                # group don't has category (group name equal category name) case
                group_to_categorized_entries_set = GroupToCategorizedEntriesSet(def_group)
                category_to_entries_set: CategoryToEntriesSet = category_to_entries_map.get_category_to_entries_set(
                    def_group)
                group_to_categorized_entries_set.add_entries_to_non_category(category_to_entries_set.entry_list)
                self.__group_to_categorized_entries[def_group] = group_to_categorized_entries_set
            else:
                # group has category case
                group_to_categorized_entries_set = GroupToCategorizedEntriesSet(def_group)
                for def_category in def_categories:
                    if category_to_entries_map.is_exist_category(def_category):
                        category_to_entries_set = category_to_entries_map.get_category_to_entries_set(def_category)
                        group_to_categorized_entries_set.add_category_to_entries_set(category_to_entries_set)
                self.__group_to_categorized_entries[def_group] = group_to_categorized_entries_set

    def __init_non_exist_category_in_definition(self, category_group_def: CategoryGroupDef,
                                                category_to_entries_map: CategoryToEntriesMap):
        for category in category_to_entries_map.categories:
            if not category_group_def.has_group_or_category(category):
                category_to_entries_set = category_to_entries_map.get_category_to_entries_set(category)
                self.__group_to_categorized_entries[NON_CATEGORY_GROUP_NAME].add_category_to_entries_set(
                    category_to_entries_set)

    def has_group(self, group) -> bool:
        return group in self.__group_to_categorized_entries

    def get_entries(self, group: str, category: Optional[str] = None) -> List[IEntry]:
        if not self.has_group(group):
            return []
        categorized_entries: GroupToCategorizedEntriesSet = self.__group_to_categorized_entries[group]
        return categorized_entries.get_entries(None if category is None else category)

    def add_entries(self, category_group_def: CategoryGroupDef, entries: IEntries):
        for entry in entries.entry_list:
            group = category_group_def.get_belongs_group(entry.top_category)
            categorized_entries: GroupToCategorizedEntriesSet = self.__group_to_categorized_entries[group]
            categorized_entries.add_entry(entry)

    def convert_md_lines(self) -> List[str]:
        def __get_entries_for_md() -> IConvertibleMarkdownLines:
            return self.__group_to_categorized_entries[group]

        lines = []
        for group in self.__sorted_groups:
            if self.has_group(group):
                lines = lines + __get_entries_for_md().convert_md_lines()
        return lines

    def dump_all_data(self, file_path):
        def build_entries_dump_data(entry_list: List[IEntry]):
            dump_entries = {}
            for entry in entry_list:
                dump_entries |= entry.build_id_to_title()
            return dump_entries

        def build_category_to_entries_dump_data(category_to_entries_list: List[CategoryToEntriesSet]):
            dump_category_to_entries = {}
            for category_to_entries_set in category_to_entries_list:
                dump_entries = build_entries_dump_data(category_to_entries_set.entry_list)
                dump_category_to_entries[category_to_entries_set.category] = dump_entries
            return dump_category_to_entries

        def build_group_to_categorized_entries_dump_data():
            dump_groups = {}
            for group in self.__sorted_groups:
                group_to_categorized_entries: GroupToCategorizedEntriesSet = self.__group_to_categorized_entries[group]
                dump_categories_and_entries = build_category_to_entries_dump_data(
                    group_to_categorized_entries.category_to_entries_list)
                # There is also entry directly under the group
                dump_entries = build_entries_dump_data(group_to_categorized_entries.entry_list_of_non_category)
                if len(dump_entries) > 0:
                    dump_categories_and_entries['-'] = dump_entries
                dump_groups[group] = dump_categories_and_entries
            return dump_groups

        dump_all_data = build_group_to_categorized_entries_dump_data()
        dump_json(file_path, dump_all_data)

    def __add_group_to_categorized_entries(self, group: str,
                                           group_to_categorized_entries: GroupToCategorizedEntriesSet):
        self.__sorted_groups.append(group)
        self.__group_to_categorized_entries[group] = group_to_categorized_entries

    @classmethod
    def deserialize_docs_grouping_data(cls, category_group_def: CategoryGroupDef,
                                       group_to_categorized_entries: Dict[str, Dict[str, Dict[str, str]]]) \
            -> GroupToCategorizedEntriesMap:
        self = GroupToCategorizedEntriesMap(category_group_def)
        for group in category_group_def.groups:
            category_to_entries_map = CategoryToEntriesMap.deserialize_docs_grouping_data(
                group_to_categorized_entries[group])
            group_to_categorized_entries_set = \
                GroupToCategorizedEntriesSet.deserialize_docs_grouping_data(group, category_to_entries_map)
            self.__add_group_to_categorized_entries(group, group_to_categorized_entries_set)
        return self
