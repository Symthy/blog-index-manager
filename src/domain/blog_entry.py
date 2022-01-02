from datetime import datetime
from typing import List

from domain.interface import IConvertibleMarkdownData
from file.file_accessor import read_text_file, dump_json, load_json


class BlogEntry:
    def __init__(self, id: str, title: str, content: str, url: str, updated: str, categories: List[str]):
        self.__id = id
        self.__title = title
        self.__content = content
        self.__url = url
        # format: 2013-09-02T11:28:23+09:00
        self.__last_updated = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%S%z")
        self.__categories = categories

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def content(self):
        return self.__content

    @property
    def url(self):
        return self.__url

    @property
    def updated(self) -> datetime:
        return self.__last_updated

    def get_updated_month_day(self) -> str:
        return self.__last_updated.strftime('%Y/%m')

    @property
    def top_category(self) -> str:
        if self.is_non_category():
            return 'Others'
        return self.__categories[0]

    def is_non_category(self) -> bool:
        return len(self.__categories) <= 0

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.url}) ({self.get_updated_month_day()})'


class BlogEntries(IConvertibleMarkdownData):
    def __init__(self, entries: List[BlogEntry] = None):
        if entries is None:
            self.__entries: List[BlogEntry] = []
        else:
            self.__entries = entries

    @property
    def items(self) -> List[BlogEntry]:
        return self.__entries

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def add_entry(self, blog_entry: BlogEntry):
        self.__entries.append(blog_entry)

    def add_entries(self, blog_entries: List[BlogEntry]):
        self.__entries.extend(blog_entries)

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.__entries]

    def update_all_entry_list_file(self):
        BLOG_ENTRIES_JSON_PATH = '../out/hatena_blog_entries.json'
        EXCLUDE_ENTRY_IDS_TXT_PATH = '../definitions/exclude_entry_ids.txt'
        exclude_ids = read_text_file(EXCLUDE_ENTRY_IDS_TXT_PATH)

        entries_json = load_json(BLOG_ENTRIES_JSON_PATH)
        for entry in self.__entries:
            if not entry.id in entries_json and entry.id in exclude_ids:
                entries_json[entry.id] = entry.title
        dump_json(BLOG_ENTRIES_JSON_PATH, entries_json)
