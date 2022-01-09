from typing import Optional

from blogs.hatena.api_executor import execute_get_hatena_all_entry_api
from common.constant import HATENA_BLOG_ENTRY_LIST_PATH, HATENA_BLOG_ENTRY_INDEX_RESULT_PATH
from domain.blog_entry import BlogEntries
from domain.category_to_entries import CategoryToEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from domain.interface import IConvertibleMarkdownLines
from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef
from file.file_accessor import write_text_lines
from file.md_data_handler import join_lines


def print_md_lines(data: IConvertibleMarkdownLines):
    # for debug
    print(join_lines(data.convert_md_lines()))


def collect_hatena_entry_local_list(blog_config: BlogConfig,
                                    category_group_def: CategoryGroupDef) -> GroupToCategorizedEntriesMap:
    """
    ブログから全記事を取得し、各記事情報をダンプ＆カテゴリ毎に分類した一覧をmdファイルに出力
    :param category_group_def:
    :param blog_config:
    :return:
    """
    blog_entries_opt: Optional[BlogEntries] = execute_get_hatena_all_entry_api(blog_config)
    if blog_entries_opt is None:
        return
    # print_md_lines(blog_entries)
    blog_entries_opt.dump_all_data()
    category_to_entries = CategoryToEntriesMap(blog_entries_opt)
    # print_md_lines(category_to_entries)
    entries_index_map = GroupToCategorizedEntriesMap(category_group_def, category_to_entries)
    print_md_lines(entries_index_map)
    write_text_lines(HATENA_BLOG_ENTRY_INDEX_RESULT_PATH, entries_index_map.convert_md_lines())
    # Todo: update blog to doc mapping
    return entries_index_map
