from typing import List, Dict

from common.constant import NON_CATEGORY_NAME
from domain.blog_entry import BlogEntries, BlogEntry
from domain.interface import IConvertibleMarkdownData


class CategoryToBlogEntriesSet(IConvertibleMarkdownData):
    def __init__(self, top_category: str):
        self.__category = top_category
        self.__blog_entries = BlogEntries()

    @property
    def category(self):
        return self.__category

    @property
    def blog_entry_list(self) -> List[BlogEntry]:
        return self.__blog_entries.items

    def is_empty(self):
        return self.__blog_entries.is_empty()

    def add_blog_entry(self, blog_entry: BlogEntry):
        self.__blog_entries.add_entry(blog_entry)

    def convert_md_lines(self) -> List[str]:
        lines = [f'- {self.category}']
        entry_md_lines = list(
            map(lambda entry: '  ' + entry.convert_md_line(), self.__blog_entries.items))
        lines = lines + entry_md_lines
        return lines


class CategoryToBlogEntriesMap(IConvertibleMarkdownData):
    def __init__(self, blog_entries: BlogEntries):
        self.__category_to_entries: Dict[str, CategoryToBlogEntriesSet] = {}
        self.__sorted_categories: List[str] = []
        for blog_entry in blog_entries.items:
            category = NON_CATEGORY_NAME if blog_entry.is_non_category() else blog_entry.top_category
            if not category in self.__category_to_entries:
                category_to_entries_set = CategoryToBlogEntriesSet(category)
                category_to_entries_set.add_blog_entry(blog_entry)
                self.__category_to_entries[category] = category_to_entries_set
                if category != NON_CATEGORY_NAME:
                    # because: Others is last in categories
                    self.__sorted_categories.append(category)
            else:
                self.__category_to_entries[category].add_blog_entry(blog_entry)

        self.__sorted_categories.sort()
        self.__sorted_categories.append(NON_CATEGORY_NAME)

    @property
    def categories(self) -> List[str]:
        return self.__sorted_categories

    def is_exist_category(self, category) -> bool:
        return category in self.__category_to_entries

    def get_category_to_entries(self, category) -> CategoryToBlogEntriesSet:
        return self.__category_to_entries[category]

    def convert_md_lines(self) -> List[str]:
        lines = []
        for category in self.__sorted_categories:
            lines = lines + self.__category_to_entries[category].convert_md_lines()
        return lines
