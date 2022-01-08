from __future__ import annotations

from typing import List, Dict, Optional

from common.constant import NON_CATEGORY_OTHERS
from domain.doc_entry import DocEntries
from domain.interface import IConvertibleMarkdownLines, IEntries, IEntry


class CategoryToEntriesSet(IConvertibleMarkdownLines):
    def __init__(self, top_category: str):
        self.__category = top_category
        self.__entry_list: List[IEntry] = []

    @property
    def category(self):
        return self.__category

    @property
    def entry_list(self) -> List[IEntry]:
        return self.__entry_list

    def is_empty(self):
        return len(self.__entry_list) == 0

    def add_entry(self, entry: IEntry):
        self.__entry_list.append(entry)

    def convert_md_lines(self) -> List[str]:
        lines = [f'- {self.category}']
        entry_md_lines = list(
            map(lambda entry: '  ' + entry.convert_md_line(), self.__entry_list))
        lines = lines + entry_md_lines
        return lines

    @classmethod
    def __init_from_dump_data(cls, category: str, entries: IEntries) -> CategoryToEntriesSet:
        self = CategoryToEntriesSet(category)
        self.__entry_list = entries.get_entries()
        return self

    @classmethod
    def deserialize_docs_grouping_data(cls, category: str, entries: IEntries) -> CategoryToEntriesSet:
        return CategoryToEntriesSet.__init_from_dump_data(category, entries)


class CategoryToEntriesMap(IConvertibleMarkdownLines):
    def __init__(self, entries: IEntries = None):
        self.__sorted_categories: List[str] = []
        self.__category_to_entries: Dict[str, CategoryToEntriesSet] = {}
        if entries is None:
            return
        for entry in entries.get_entries():
            category = entry.top_category
            if not category in self.__category_to_entries:
                category_to_entries_set = CategoryToEntriesSet(category)
                category_to_entries_set.add_entry(entry)
                self.__category_to_entries[category] = category_to_entries_set
                if category != NON_CATEGORY_OTHERS:
                    # because: Others is last in categories
                    self.__sorted_categories.append(category)
            else:
                self.__category_to_entries[category].add_entry(entry)
        self.__sorted_categories.sort()
        self.__sorted_categories.append(NON_CATEGORY_OTHERS)

    @property
    def categories(self) -> List[str]:
        return self.__sorted_categories

    @property
    def category_to_entries_sets(self) -> List[CategoryToEntriesSet]:
        return list(self.__category_to_entries.values())

    def pop(self, category: str) -> Optional[CategoryToEntriesSet]:
        if category in self.__category_to_entries:
            return self.__category_to_entries.pop(category)
        return None

    def is_empty(self) -> bool:
        return len(self.__category_to_entries) == 0

    def is_exist_category(self, category) -> bool:
        return category in self.__category_to_entries

    def get_category_to_entries_set(self, category: str = None) -> CategoryToEntriesSet:
        return self.__category_to_entries[category]

    def convert_md_lines(self) -> List[str]:
        lines = []
        for category in self.__sorted_categories:
            lines = lines + self.__category_to_entries[category].convert_md_lines()
        return lines

    def __add_category_to_entries(self, category: str, category_to_entries: CategoryToEntriesSet):
        self.__sorted_categories.append(category)
        self.__category_to_entries[category] = category_to_entries

    @classmethod
    def deserialize_docs_grouping_data(cls, category_to_entries_obj: Dict[str, Dict[str, str]]) -> CategoryToEntriesMap:
        self = CategoryToEntriesMap()
        for category, entries in category_to_entries_obj.items():
            doc_entries = DocEntries.deserialize_grouping_data(category, entries)
            category_to_entries_set = CategoryToEntriesSet.deserialize_docs_grouping_data(category, doc_entries)
            self.__add_category_to_entries(category, category_to_entries_set)
        return self
