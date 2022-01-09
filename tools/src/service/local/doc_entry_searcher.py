from typing import List

from common.constant import NON_CATEGORY_GROUP_NAME
from docs.docs_data_deserializer import deserialize_doc_entry_grouping_data
from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IEntry
from file.category_group_def import CategoryGroupDef


class EntrySearchResults:
    LINE_FORMAT = '{0:<16} {1:<30} {2:<15} {3<15}'

    class EntrySearchResult:
        def __init__(self, entry_id, title, group, category):
            self.__id = entry_id
            self.__title = title
            self.__group = group
            self.__category = category

        def print_entry_search_result(self):
            print(EntrySearchResults.LINE_FORMAT.format(self.__id, self.__title, self.__group, self.__category))

    def __init__(self, entries: List[IEntry], group: str):
        self.__results = []
        for entry in entries:
            self.__results.append(
                EntrySearchResults.EntrySearchResult(entry.id, entry.title, group, entry.top_category))

    def print_entry_search_results(self):
        for result in self.__results:
            result.print_entry_search_result()

    @classmethod
    def print_header_line(cls):
        hyphen = '-'
        print(EntrySearchResults.LINE_FORMAT.format('[Entry ID]', '[Entry Title]', '[Group]', '[Category]'))
        print(f'{hyphen:->16} {hyphen:->30} {hyphen:->15} {hyphen:->15}')


def __print_search_results(results: EntrySearchResults):
    EntrySearchResults.print_header_line()
    results.print_entry_search_results()


def search_doc_entry_by_group(category_group_def: CategoryGroupDef, group: str):
    grouping_data: GroupToCategorizedEntriesMap = deserialize_doc_entry_grouping_data(category_group_def)
    if not category_group_def.has_group_case_insensitive(group):
        print(f'[Warn] Nothing specified group: {group}')
        return
    entries: List[IEntry] = grouping_data.get_entries(group)
    __print_search_results(EntrySearchResults(entries, group))


def search_doc_entry_by_category(category_group_def: CategoryGroupDef, category: str):
    def print_entries_in_category(group_name: str, category_name: str):
        entries: List[IEntry] = grouping_data.get_entries(group_name, category_name)
        if len(entries) == 0:
            print(f'[Warn] Nothing docs of specified category: {category}')
        __print_search_results(EntrySearchResults(entries, group))

    grouping_data: GroupToCategorizedEntriesMap = deserialize_doc_entry_grouping_data(category_group_def)
    is_exist_category = category_group_def.has_category(category)
    group = category_group_def.get_belongs_group(category)
    if not is_exist_category and group == NON_CATEGORY_GROUP_NAME:
        # Docs with no categories in the definition are under NON_CATEGORY_GROUP_NAME
        print_entries_in_category(NON_CATEGORY_GROUP_NAME, category)
        return
    if is_exist_category:
        print_entries_in_category(group, category)
        return
    print(f'[Warn] Nothing specified category: {category}')
