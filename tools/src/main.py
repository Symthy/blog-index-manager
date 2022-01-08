import sys
from typing import List

from blogs.hatena.api_executor import execute_put_hatena_summary_entry, \
    execute_get_hatena_specified_entry_api
from common.constant import BLOG_CONF_PATH
from docs.document_initializer import new_local_document_set, initialize_docs_dir
from domain.interface import IConvertibleMarkdownLines
from file.blog_config import BlogConfig
from file.file_accessor import read_blog_config, load_category_group_def_yaml
from service.local.doc_entry_pusher import push_documents_to_docs
from service.local.doc_entry_retriever import retrieve_document_from_docs, cancel_retrieving_document
from templates.hatena_entry_format import get_blog_summary_index_content


def print_md_lines(data: IConvertibleMarkdownLines):
    # for debug
    print(join_lines(data.convert_md_lines()))


def show_hatena_entry(blog_config: BlogConfig, entry_id):
    # for debug
    blog_entry = execute_get_hatena_specified_entry_api(blog_config, entry_id)
    print(blog_entry.content)


def join_lines(lines: List[str]) -> str:
    data = ''
    for line in lines:
        data = data + line + '\n'
    return data


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


def main(args: List[str], is_debug: bool):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    category_group_def = load_category_group_def_yaml()
    # entries_index_map = update_hatena_entry_local_list(blog_config, category_group_def)
    # put_hatena_summary_page(blog_config, entries_index_map)

    # show_hatena_entry(blog_config, '26006613443907494')
    # TODO: use argparse? (no use docopt. because last update is old)
    if len(args) >= 2 and (args[1] == '-init' or args[1] == '-i'):
        initialize_docs_dir(category_group_def)
        print('Success: created \"docs\" dir')
        return
    if len(args) >= 2 and (args[1] == '-new' or args[1] == '-n'):
        title_value = new_local_document_set(args)
        print(f'Success: created \"{title_value}\" dir in work dir')
        return
    if len(args) >= 2 and (args[1] == '-push' or args[1] == '-p'):
        target_dirs = args[2:] if len(args) > 2 else []
        push_documents_to_docs(category_group_def, target_dirs)
        print('Success: push doc data to docs dir')
        return
    if len(args) >= 2 and (args[1] == '-retrieve' or args[1] == '-ret' or args[1] == '-r'):
        if len(args) >= 3 and (args[2] == '-cancel' or args[2] == '-c'):
            cancel_retrieving_document(args[3:])
        else:
            retrieve_document_from_docs(args[2:])
        print('Success: retrieve doc data to work dir')
        return
    if len(args) >= 2 and (args[1] == '-search' or args[1] == '-s'):
        print('Unimplemented')
        return
    if len(args) >= 2 and (args[1] == '-delete' or args[1] == '-d'):
        print('Unimplemented')
        return
    if len(args) >= 2 and (args[1] == '-blog' or args[1] == '-b'):
        print('Unimplemented')
        return


IS_DEBUG = False
main(sys.argv, IS_DEBUG)
