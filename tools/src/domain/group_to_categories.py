import copy
from typing import List, Dict

from domain.blog_entry import BlogEntries, BlogEntry
from domain.category_to_entries import CategoryToBlogEntriesMap, CategoryToBlogEntriesSet, NON_CATEGORY_NAME
from domain.interface import IConvertibleMarkdownData
from file.category_group_def import CategoryGroupDef


class GroupToCategorizedEntriesSet(IConvertibleMarkdownData):
    def __init__(self, group: str):
        self.__group = group
        self.__categories = []
        self.__category_to_entries: List[CategoryToBlogEntriesSet] = []
        self.__entries: BlogEntries = BlogEntries()

    def add_category_to_entries(self, category_to_entries: CategoryToBlogEntriesSet):
        if category_to_entries.is_empty():
            return
        self.__categories.append(category_to_entries.category)
        self.__category_to_entries.append(category_to_entries)

    def add_entries(self, entries: List[BlogEntry]):
        self.__entries.add_entries(entries)

    def get_categorized_entries(self) -> List[IConvertibleMarkdownData]:
        ret_list: List[IConvertibleMarkdownData] = copy.deepcopy(self.__category_to_entries)
        ret_list.append(self.__entries)
        return ret_list

    def is_empty(self) -> bool:
        return len(self.__category_to_entries) == 0 and self.__entries.is_empty()

    def convert_md_lines(self) -> List[str]:
        lines = [f'- {self.__group}']
        for category_to_entries in self.get_categorized_entries():
            category_to_entries_lines = list(map(lambda line: '  ' + line, category_to_entries.convert_md_lines()))
            lines = lines + category_to_entries_lines
        return lines


class GroupToCategorizedEntriesMap(IConvertibleMarkdownData):
    def __init__(self, category_to_entries_map: CategoryToBlogEntriesMap, category_group_def: CategoryGroupDef):
        self.__sorted_groups: List[str] = []
        self.__group_to_categorized_entries: Dict[str, GroupToCategorizedEntriesSet] = {}
        self.__init_based_category_group_def(category_group_def, category_to_entries_map)
        self.__init_non_exist_category_in_definition(category_group_def, category_to_entries_map)

    def __init_based_category_group_def(self, category_group_def: CategoryGroupDef,
                                        category_to_entries_map: CategoryToBlogEntriesMap):
        for grouping_categories in category_group_def.grouping_categories:
            def_group = grouping_categories.group_name
            def_categories = grouping_categories.categories
            self.__sorted_groups.append(def_group)  # the order of groups follows the definition(category_group.yml)
            if category_to_entries_map.is_exist_category(def_group):
                # group don't has category (group name equal category name) case
                group_to_categorized_entries_set = GroupToCategorizedEntriesSet(def_group)
                category_to_entries_set = category_to_entries_map.get_category_to_entries(def_group)
                group_to_categorized_entries_set.add_entries(category_to_entries_set.blog_entry_list)
                self.__group_to_categorized_entries[def_group] = group_to_categorized_entries_set
            else:
                # group has category case
                group_to_categorized_entries_set = GroupToCategorizedEntriesSet(def_group)
                for def_category in def_categories:
                    if category_to_entries_map.is_exist_category(def_category):
                        category_to_entries_set = category_to_entries_map.get_category_to_entries(def_category)
                        group_to_categorized_entries_set.add_category_to_entries(category_to_entries_set)
                # if not group_to_categorized_entries_set.is_empty():
                self.__group_to_categorized_entries[def_group] = group_to_categorized_entries_set

    def __init_non_exist_category_in_definition(self, category_group_def: CategoryGroupDef,
                                                category_to_entries_map: CategoryToBlogEntriesMap):
        # add entries that non exist category in category group definition
        for category in category_to_entries_map.categories:
            if category_group_def.is_non_exist_group_or_category(category):
                category_to_entries_set = category_to_entries_map.get_category_to_entries(category)
                self.__group_to_categorized_entries[NON_CATEGORY_NAME].add_category_to_entries(category_to_entries_set)

    def has_group(self, group) -> bool:
        return group in self.__group_to_categorized_entries

    def __get_entries_for_md(self, group) -> IConvertibleMarkdownData:
        return self.__group_to_categorized_entries[group]

    def convert_md_lines(self) -> List[str]:
        lines = []
        for group in self.__sorted_groups:
            if self.has_group(group):
                lines = lines + self.__get_entries_for_md(group).convert_md_lines()
        return lines
