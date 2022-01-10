from typing import Optional

from blogs.hatena.api_executor import execute_put_hatena_summary_page, execute_post_hatena_blog_entry_register_api, \
    execute_put_hatena_blog_entry_update_api
from domain.blog.blog_entry import BlogEntry
from domain.group_to_categories import GroupToCategorizedEntriesMap
from file.blog_config import BlogConfig
from file.file_accessor import read_md_file
from file.md_data_handler import join_lines
from blogs.hatena.templates.hatena_entry_format import get_blog_summary_index_content


def put_hatena_summary_page(blog_config: BlogConfig, entries_index_map: GroupToCategorizedEntriesMap):
    """
    ブログのトップページ(summary)を更新する
    :param blog_config:
    :param entries_index_map:
    :return:
    """
    content = get_blog_summary_index_content().format(md_lines=join_lines(entries_index_map.convert_md_lines()))
    is_success = execute_put_hatena_summary_page(blog_config, content)
    if not is_success:
        print('[Error] blog summary page update failure')


def __build_md_file_path(dir_path: str, md_file_name: str):
    return dir_path + md_file_name


def push_hatena_blog_entry(blog_config, dir_path: str, md_file_name: str, title: str, category: str,
                           blog_entry_id: str = None) -> Optional[BlogEntry]:
    md_file_path = __build_md_file_path(dir_path, md_file_name)
    content = read_md_file(md_file_path)
    if blog_entry_id is None:
        return execute_post_hatena_blog_entry_register_api(blog_config, title, category, content)
    else:
        return execute_put_hatena_blog_entry_update_api(blog_config, blog_entry_id, title, category, content)
