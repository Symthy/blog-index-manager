from datetime import datetime
from typing import List, Optional

from domain.interface import IConvertibleMarkdownData
from file.file_accessor import read_text_file, dump_json, load_json
from ltime.time_resolver import resolve_current_time, convert_datetime_to_str


class BlogEntry:
    def __init__(self, entry_id: str, title: str, content: str, url: str, api_url: str,
                 last_updated: Optional[datetime], categories: List[str]):
        self.__id = entry_id
        self.__title = title
        self.__content = content
        self.__url = url
        self.__api_url = api_url
        # Make it optional just in case
        self.__last_updated: Optional[datetime] = last_updated
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
    def api_url(self):
        return self.__api_url

    def get_updated_month_day(self) -> str:
        if self.__last_updated is None:
            return 'unknown'
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

    def build_dump_data(self) -> object:
        return {
            "id": self.__id,
            "title": self.__title,
            "category": self.top_category,
            "categories": self.__categories,
            "url": self.__url,
            "api_url": self.__api_url,
            "updated_time": convert_datetime_to_str(self.__last_updated),
            "local_path": "",  # TODO
            "pictures": {}  # TODO
        }


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
        HATENA_BLOG_ENTRY_DUMP_DIR = '../out/hatena_entry_data/'
        HATENA_BLOG_ENTRY_LIST_PATH = '../out/hatena_entry_list.json'
        EXCLUDE_ENTRY_IDS_TXT_PATH = '../definitions/exclude_entry_ids.txt'
        exclude_ids = read_text_file(EXCLUDE_ENTRY_IDS_TXT_PATH)

        json_data = load_json(HATENA_BLOG_ENTRY_LIST_PATH)
        json_data['updated_time'] = resolve_current_time()
        json_entries = {}
        if 'entries' in json_data:
            json_entries = json_data['entries']
        for entry in self.__entries:
            if not entry.id in json_entries and not entry.id in exclude_ids:
                json_entries[entry.title] = entry.id
                dump_json(f'{HATENA_BLOG_ENTRY_DUMP_DIR}/{entry.id}.json', entry.build_dump_data())
        # dump data format
        # {
        #   "updated_time": "2022-01-02T03:04:05",
        #   "entries": {
        #     "entry_id": "entry title"
        #      :
        #   }
        # }
        json_data['entries'] = json_entries
        dump_json(HATENA_BLOG_ENTRY_LIST_PATH, json_data)
