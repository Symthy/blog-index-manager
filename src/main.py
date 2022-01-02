from typing import List

from api.api_executor import execute_get_entry_list_api
from api.response_parser import parse_blog_entries_xml
from domain.category_to_entries import CategoryToBlogEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from file.file_accessor import read_blog_config, write_text_file

CONF_DIR_PATH = '../conf/'
OUT_DIR_PATH = '../out/'
BLOG_CONF_PATH = CONF_DIR_PATH + 'blog.conf'
BLOG_ENTRIES_INDEX_PATH = OUT_DIR_PATH + 'all_entry_index_content.md'


# for debug
def print_md_lines(lines: List[str]):
    md_data = ''
    for line in lines:
        md_data = md_data + line + '\n'
    print(md_data)


def main(is_debug: bool):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    response_xml = execute_get_entry_list_api(blog_config)
    blog_entries = parse_blog_entries_xml(response_xml)
    print_md_lines(blog_entries.convert_md_lines())
    # breaking: blog_entries.update_all_entry_list_file()
    category_to_entries = CategoryToBlogEntriesMap(blog_entries)
    print_md_lines(category_to_entries.convert_md_lines())
    entries_index_map = GroupToCategorizedEntriesMap(category_to_entries)
    print_md_lines(entries_index_map.convert_md_lines())
    write_text_file(BLOG_ENTRIES_INDEX_PATH, entries_index_map.convert_md_lines())


IS_DEBUG = False
main(IS_DEBUG)
