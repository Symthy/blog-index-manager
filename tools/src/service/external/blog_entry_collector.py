from typing import Optional

from blogs.hatena.api_executor import execute_get_hatena_all_entry_api
from domain.blog_entry import BlogEntries
from domain.interface import IConvertibleMarkdownLines
from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef
from file.md_data_handler import join_lines
from service.external.blog_entry_index_updater import update_blog_entry_index


def print_md_lines(data: IConvertibleMarkdownLines):
    # for debug
    print(join_lines(data.convert_md_lines()))


def collect_hatena_entry_local_list(blog_config: BlogConfig,
                                    category_group_def: CategoryGroupDef):
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
    update_blog_entry_index(category_group_def, blog_entries_opt)
    # Todo: reflection of deleted blog entry
