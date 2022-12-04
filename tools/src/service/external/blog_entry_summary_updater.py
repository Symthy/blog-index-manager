from blogs.api.interface import IBlogApiExecutor
from blogs.hatena.templates.hatena_entry_format import get_blog_summary_index_template
from common.constant import HATENA_BLOG_ENTRY_INDEX_RESULT_PATH
from files.file_accessor import write_text_lines
from files.md_data_handler import join_lines
from service.entry_summary_factory import EntrySummaryFactory


def update_blog_entry_summary_file(entry_summary_factory: EntrySummaryFactory):
    blog_entry_summary = entry_summary_factory.build_blog_entry_summary()
    write_text_lines(HATENA_BLOG_ENTRY_INDEX_RESULT_PATH, blog_entry_summary.all_entry_lines)


def put_hatena_summary_page(api_executor: IBlogApiExecutor, entry_summary_factory: EntrySummaryFactory) -> bool:
    """
    ブログのトップページ(summary)を更新する
    :param api_executor:
    :param entry_summary_factory:
    :return:
    """
    entry_summary = entry_summary_factory.build_blog_entry_summary()
    content = get_blog_summary_index_template().format(md_lines=join_lines(entry_summary.pickup_and_all_entry_lines()))
    is_success = api_executor.execute_update_blog_summary_page(content)
    return is_success
