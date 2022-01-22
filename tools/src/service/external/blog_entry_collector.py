from blogs.api.interface import IBlogApiExecutor
from domain.blog.blog_entry import BlogEntries
from domain.interface import IConvertibleMarkdownLines
from files.conf.category_group_def import CategoryGroupDef
from files.md_data_handler import join_lines
from service.external.blog_entry_index_updater import update_blog_entry_summary_index_file


def print_md_lines(data: IConvertibleMarkdownLines):
    # for debug
    print(join_lines(data.convert_md_lines()))


def collect_hatena_entry_local_list(api_executor: IBlogApiExecutor, category_group_def: CategoryGroupDef):
    """
    ブログから全記事を取得し、各記事情報をダンプ＆カテゴリ毎に分類した一覧をmdファイルに出力
    :param api_executor:
    :param category_group_def:
    :return:
    """
    blog_entries: BlogEntries = api_executor.execute_get_all_blog_entries_api()
    if blog_entries.is_empty():
        return
    # print_md_lines(blog_entries)
    blog_entries.dump_all_data()
    update_blog_entry_summary_index_file(category_group_def, blog_entries)
    # Todo: reflection of deleted blog entry
