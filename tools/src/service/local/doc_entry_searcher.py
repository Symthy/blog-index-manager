from __future__ import annotations

from typing import List, Dict, Optional

from common.constant import NON_CATEGORY_GROUP_NAME
from docs.docs_grouping_deserializer import deserialize_doc_entry_grouping_data
from domain.doc.doc_entry import DocEntries
from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IEntry, IEntries
from dump.blog_to_doc_mapping import BlogDocEntryMapping
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import load_docs_entries_json


class EntrySearchResults:
    LINE_FORMAT = '{0:<15} {1:<32} {2:<15} {3:<15} {4:<11}'

    class EntrySearchResult:
        def __init__(self, entry_id, title, group, category, blog_id: Optional[str] = None):
            self.__id = entry_id
            self.__title = title
            self.__group = group
            self.__category = category
            self.__is_blog_posted = 'True' if blog_id is not None else 'False'

        def print_entry_search_result(self):
            print(EntrySearchResults.LINE_FORMAT.format(self.__id, self.__title, self.__group, self.__category,
                                                        self.__is_blog_posted))

    def __init__(self):
        self.__results = []

    @classmethod
    def print_header_line(cls):
        hyphen = '-'
        print(EntrySearchResults.LINE_FORMAT
              .format('Doc Entry ID', 'Doc Entry Title', 'Group Name', 'Category Name', 'Blog Posted'))
        print(f'{hyphen:->15} {hyphen:->32} {hyphen:->15} {hyphen:->15} {hyphen:->11}')

    @classmethod
    def init_by_single_group(cls, group: str, entries: List[IEntry]) -> EntrySearchResults:
        blog_doc_mapping = BlogDocEntryMapping()
        self = EntrySearchResults()
        for entry in entries:
            blog_id_opt = blog_doc_mapping.get_blog_entry_id(entry.id)
            self.__results.append(
                EntrySearchResults.EntrySearchResult(entry.id, entry.title, group, entry.top_category, blog_id_opt))
        return self

    @classmethod
    def init_by_multi_groups(cls, category_group_def: CategoryGroupDef, entries: IEntries) -> EntrySearchResults:
        blog_doc_mapping = BlogDocEntryMapping()
        self = EntrySearchResults()
        for entry in entries.entry_list:
            group = category_group_def.get_belongs_group(entry.top_category)
            blog_id_opt = blog_doc_mapping.get_blog_entry_id(entry.id)
            self.__results.append(
                EntrySearchResults.EntrySearchResult(entry.id, entry.title, group, entry.top_category, blog_id_opt))
        return self

    def __print_entry_search_results(self):
        for result in self.__results:
            result.print_entry_search_result()

    def print_search_results(self):
        EntrySearchResults.print_header_line()
        self.__print_entry_search_results()


def search_doc_entry_by_group(category_group_def: CategoryGroupDef, group: str):
    grouping_data: GroupToCategorizedEntriesMap = deserialize_doc_entry_grouping_data(category_group_def)
    if not category_group_def.has_group_case_insensitive(group):
        print(f'[Warn] Nothing specified group: {group}')
        return
    entries: List[IEntry] = grouping_data.get_entries(group)
    EntrySearchResults.init_by_single_group(group, entries).print_search_results()


def search_doc_entry_by_category(category_group_def: CategoryGroupDef, category: str):
    def print_entries_in_category(group_name: str, category_name: str):
        entries: List[IEntry] = grouping_data.get_entries(group_name, category_name)
        if len(entries) == 0:
            print(f'[Warn] Nothing docs of specified category: {category_name}')
        EntrySearchResults.init_by_single_group(group_name, entries).print_search_results()

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


def search_doc_entry_by_title(category_group_def: CategoryGroupDef, keyword: str):
    def resolve_title_partial_match_doc_entry(search_word: str) -> List[str]:
        entry_id_to_title: Dict[str, str] = load_docs_entries_json()
        ids = []
        for eid, title in entry_id_to_title.items():
            if search_word in title:
                ids.append(eid)
        return ids

    entry_ids: List[str] = resolve_title_partial_match_doc_entry(keyword)
    if len(entry_ids) == 0:
        print(f'[Warn] Nothing partially matched doc title: {keyword}')
    entries = DocEntries.init_from_entry_ids(entry_ids)
    EntrySearchResults.init_by_multi_groups(category_group_def, entries).print_search_results()
