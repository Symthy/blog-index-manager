from typing import List

from api.hatena_api_executor import execute_get_hatena_entry_list_api
from api.hatena_api_executor import execute_put_hatena_summary_entry
from api.response_parser import parse_blog_entries_xml
from domain.category_to_entries import CategoryToBlogEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from file.blog_config import BlogConfig
from file.file_accessor import read_blog_config, write_text_file

CONF_DIR_PATH = '../conf/'
OUT_DIR_PATH = '../out/'
BLOG_CONF_PATH = CONF_DIR_PATH + 'blog.conf'
BLOG_ENTRIES_INDEX_PATH = OUT_DIR_PATH + 'summary_entry_index_result.md'


# for debug
def print_md_lines(lines: List[str]):
    print(join_lines(lines))


def join_lines(lines: List[str]) -> str:
    data = ''
    for line in lines:
        data = data + line + '\n'
    return data


def update_hatena_entry_local_list(blog_config: BlogConfig) -> GroupToCategorizedEntriesMap:
    response_xml = execute_get_hatena_entry_list_api(blog_config)
    print(response_xml)
    blog_entries = parse_blog_entries_xml(response_xml)
    print_md_lines(blog_entries.convert_md_lines())
    blog_entries.update_all_entry_list_file()
    category_to_entries = CategoryToBlogEntriesMap(blog_entries)
    print_md_lines(category_to_entries.convert_md_lines())
    entries_index_map = GroupToCategorizedEntriesMap(category_to_entries)
    print_md_lines(entries_index_map.convert_md_lines())
    write_text_file(BLOG_ENTRIES_INDEX_PATH, entries_index_map.convert_md_lines())
    return entries_index_map


def put_hatena_summary_page(blog_config, entries_index_map):
    SUMMARY_CONTENT = """本ページは投稿記事一覧です。 (自動更新)

{md_lines}
    """
    content = SUMMARY_CONTENT.format(md_lines=join_lines(entries_index_map.convert_md_lines()))
    execute_put_hatena_summary_entry(blog_config, content)
    # execute_put_hatena_summary_entry(blog_config, TEST_DATA)


def main(is_debug: bool):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    entries_index_map = update_hatena_entry_local_list(blog_config)
    # put_hatena_summary_page(blog_config, entries_index_map)


IS_DEBUG = False
main(IS_DEBUG)
