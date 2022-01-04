import sys
from typing import List

from api.hatena_api_executor import execute_get_hatena_all_entry_api, execute_get_hatena_specified_entry_api
from api.hatena_api_executor import execute_put_hatena_summary_entry
from docs.document_initializer import new_local_document_set, initialize_docs_dir
from docs.document_organizer import move_documents_to_docs_dir
from domain.blog_entry import BlogEntries
from domain.category_to_entries import CategoryToBlogEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IConvertibleMarkdownData
from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef
from file.file_accessor import read_blog_config, write_text_file, load_category_group_def_yaml

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


def update_hatena_entry_local_list(blog_config: BlogConfig,
                                   category_group_def: CategoryGroupDef) -> GroupToCategorizedEntriesMap:
    """
    はてなブログから全記事を取得し、各記事情報をダンプ＆カテゴリ毎に分類した一覧をmdファイルに出力
    :param category_group_def:
    :param blog_config:
    :return:
    """
    blog_entries: BlogEntries = execute_get_hatena_all_entry_api(blog_config)
    # print_md_lines(blog_entries)
    blog_entries.dump_all_entry()
    category_to_entries = CategoryToBlogEntriesMap(blog_entries)
    # print_md_lines(category_to_entries)
    entries_index_map = GroupToCategorizedEntriesMap(category_to_entries, category_group_def)
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


def main(args: List[str], is_debug: bool):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    category_group_def = load_category_group_def_yaml()
    # entries_index_map = update_hatena_entry_local_list(blog_config, category_group_def)
    # put_hatena_summary_page(blog_config, entries_index_map)

    # show_hatena_entry(blog_config, '26006613443907494')
    # TODO: use argparse
    if len(args) >= 2 and (args[1] == '-init' or args[1] == '-i'):
        initialize_docs_dir(category_group_def)
        print('Success: created \"docs\" dir')
        return
    if len(args) >= 2 and (args[1] == '-new' or args[1] == '-n'):
        title_value = new_local_document_set(args)
        print(f'Success: created \"{title_value}\" dir in \"in\" dir')
        return
    if len(args) >= 2 and (args[1] == '-push' or args[1] == '-p'):
        target_dirs = args[2:] if len(args) > 2 else []
        move_documents_to_docs_dir(category_group_def, target_dirs)
        print('Success: move to dir')
        return


IS_DEBUG = False
main(sys.argv, IS_DEBUG)
