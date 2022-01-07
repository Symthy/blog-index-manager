from typing import List, Dict

from common.constant import NON_CATEGORY_OTHERS
from domain.interface import IConvertibleMarkdownLines, IEntries, IEntry


class CategoryToEntriesSet(IConvertibleMarkdownLines):
    def __init__(self, top_category: str):
        self.__category = top_category
        self.__entries: List[IEntry] = []

    @property
    def category(self):
        return self.__category

    @property
    def entries(self) -> List[IEntry]:
        return self.__entries

    def is_empty(self):
        return len(self.__entries) == 0

    def add_entry(self, entry: IEntry):
        self.__entries.append(entry)

    def convert_md_lines(self) -> List[str]:
        lines = [f'- {self.category}']
        entry_md_lines = list(
            map(lambda entry: '  ' + entry.convert_md_line(), self.__entries))
        lines = lines + entry_md_lines
        return lines


class CategoryToEntriesMap(IConvertibleMarkdownLines):
    def __init__(self, entries: IEntries):
        self.__category_to_entries: Dict[str, CategoryToEntriesSet] = {}
        self.__sorted_categories: List[str] = []
        for entry in entries.get_entries():
            category = entry.resolve_category()
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

    def is_exist_category(self, category) -> bool:
        return category in self.__category_to_entries

    def get_category_to_entries(self, category) -> CategoryToEntriesSet:
        return self.__category_to_entries[category]

    def convert_md_lines(self) -> List[str]:
        lines = []
        for category in self.__sorted_categories:
            lines = lines + self.__category_to_entries[category].convert_md_lines()
        return lines
