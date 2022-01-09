from blogs.hatena.api_executor import execute_put_hatena_summary_entry
from service.external.md_data_handler import join_lines

from templates.hatena_entry_format import get_blog_summary_index_content


def put_hatena_summary_page(blog_config, entries_index_map):
    """
    ブログのトップページ(summary)を更新する
    :param blog_config:
    :param entries_index_map:
    :return:
    """
    content = get_blog_summary_index_content().format(md_lines=join_lines(entries_index_map.convert_md_lines()))
    execute_put_hatena_summary_entry(blog_config, content)


def update_hatena_blog_entry(blog_config, dir_path):
    pass
