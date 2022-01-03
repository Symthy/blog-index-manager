import codecs
import os
import sys
from typing import List, Optional

from api.hatena_api_executor import execute_get_hatena_all_entry_api, execute_get_hatena_specified_entry_api
from api.hatena_api_executor import execute_put_hatena_summary_entry
from domain.blog_entry import BlogEntries
from domain.category_to_entries import CategoryToBlogEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IConvertibleMarkdownData
from file.blog_config import BlogConfig
from file.file_accessor import read_blog_config, write_text_file
from ltime.time_resolver import resolve_current_time_sequence

CONF_DIR_PATH = '../conf/'
OUT_DIR_PATH = '../out/'
BLOG_CONF_PATH = CONF_DIR_PATH + 'blog.conf'
BLOG_ENTRIES_INDEX_PATH = OUT_DIR_PATH + 'summary_entry_index_result.md'


# for debug
def print_md_lines(data: IConvertibleMarkdownData):
    print(join_lines(data.convert_md_lines()))


# for debug
def show_hatena_entry(blog_config: BlogConfig, entry_id):
    blog_entry = execute_get_hatena_specified_entry_api(blog_config, entry_id)
    print(blog_entry.content)


def join_lines(lines: List[str]) -> str:
    data = ''
    for line in lines:
        data = data + line + '\n'
    return data


def update_hatena_entry_local_list(blog_config: BlogConfig) -> GroupToCategorizedEntriesMap:
    """
    はてなブログから全記事を取得し、各記事情報をダンプ＆カテゴリ毎に分類した一覧をmdファイルに出力
    :param blog_config:
    :return:
    """
    blog_entries: BlogEntries = execute_get_hatena_all_entry_api(blog_config)
    # print_md_lines(blog_entries)
    blog_entries.dump_all_entry()
    category_to_entries = CategoryToBlogEntriesMap(blog_entries)
    # print_md_lines(category_to_entries)
    entries_index_map = GroupToCategorizedEntriesMap(category_to_entries)
    print_md_lines(entries_index_map)
    write_text_file(BLOG_ENTRIES_INDEX_PATH, entries_index_map.convert_md_lines())
    return entries_index_map


def put_hatena_summary_page(blog_config, entries_index_map):
    """
    はてなブログのトップページ(summary)を更新する
    :param blog_config:
    :param entries_index_map:
    :return:
    """
    SUMMARY_CONTENT = """本ページは投稿記事一覧です。 (自動更新)

{md_lines}
    """
    content = SUMMARY_CONTENT.format(md_lines=join_lines(entries_index_map.convert_md_lines()))
    execute_put_hatena_summary_entry(blog_config, content)


def update_hatena_blog_entry(blog_config, dir_path):
    pass


def initialize_new_local_entry(title: Optional[str], category: Optional[str]):
    if title is None:
        title = 'doc'  # default value
    if category is None:
        category = ''  # default value
    new_dir_path = '../../in/' + resolve_current_time_sequence()
    file_name = title + '.md'
    os.mkdir(new_dir_path)
    md_file_path = f'{new_dir_path}/{file_name}'
    with codecs.open(md_file_path, mode='w', encoding='utf-8') as f:
        f.write(f'# {title}\n')
    category_file_path = f'{new_dir_path}/category.txt'
    with codecs.open(category_file_path, mode='w', encoding='utf-8') as f:
        f.write(category)


def main(args: List[str], is_debug: bool):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    # entries_index_map = update_hatena_entry_local_list(blog_config)
    # put_hatena_summary_page(blog_config, entries_index_map)

    # show_hatena_entry(blog_config, '26006613443907494')
    if args[0] == '-init' or args[0] == '-i':
        title = None
        category = None
        t_index = args.index('-t')
        if t_index != -1 and len(args) >= t_index + 1:
            title = args[t_index]
        c_index = args.index('-c')
        if c_index != -1 and len(args) >= c_index + 1:
            category = args[c_index]
        initialize_new_local_entry(title, category)


IS_DEBUG = False
main(sys.argv, IS_DEBUG)
