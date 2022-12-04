from blogs.api.interface import IBlogApiExecutor
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.interface import IConvertibleMarkdownLines
from dump.interface import IDumpEntriesAccessor
from files.md_data_handler import join_lines
from service.entry_summary_factory import EntrySummaryFactory
from service.external.blog_entry_summary_updater import update_blog_entry_summary_file


def print_md_lines(data: IConvertibleMarkdownLines):
    # for debug
    print(join_lines(data.convert_md_lines()))


def collect_hatena_entry_local_list(api_executor: IBlogApiExecutor,
                                    dump_blog_data_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
                                    entry_summary_factory: EntrySummaryFactory):
    """
    ブログから全記事を取得し、各記事情報をダンプ＆カテゴリ毎に分類した一覧をmdファイルに出力（動作未保障）
    :param dump_blog_data_accessor:
    :param api_executor:
    :param entry_summary_factory:
    :return:
    """
    blog_entries: BlogEntries = api_executor.execute_get_all_blog_entries_api()
    if blog_entries.is_empty():
        return
    # print_md_lines(blog_entries)
    dump_blog_data_accessor.save_entries(blog_entries)
    update_blog_entry_summary_file(entry_summary_factory)
    # Todo: reflection of deleted blog entry
