from blogs.hatena.api_executor import execute_get_hatena_all_entry_api
from common.constant import HATENA_BLOG_ENTRY_LIST_PATH, HATENA_BLOG_ENTRY_INDEX_RESULT_PATH
from domain.blog_entry import BlogEntries
from domain.category_to_entries import CategoryToEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef
from file.file_accessor import write_text_lines
from service.external.md_data_handler import print_md_lines


def collect_hatena_entry_local_list(blog_config: BlogConfig,
                                    category_group_def: CategoryGroupDef) -> GroupToCategorizedEntriesMap:
    """
    ブログから全記事を取得し、各記事情報をダンプ＆カテゴリ毎に分類した一覧をmdファイルに出力
    :param category_group_def:
    :param blog_config:
    :return:
    """
    blog_entries: BlogEntries = execute_get_hatena_all_entry_api(blog_config)
    # print_md_lines(blog_entries)
    blog_entries.dump_all_data(HATENA_BLOG_ENTRY_LIST_PATH)
    category_to_entries = CategoryToEntriesMap(blog_entries)
    # print_md_lines(category_to_entries)
    entries_index_map = GroupToCategorizedEntriesMap(category_group_def, category_to_entries)
    print_md_lines(entries_index_map)
    write_text_lines(HATENA_BLOG_ENTRY_INDEX_RESULT_PATH, entries_index_map.convert_md_lines())
    return entries_index_map
