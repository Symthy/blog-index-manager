import sys
from typing import List

from blogs.hatena.api_executor import execute_get_hatena_specified_entry_api
from common.constant import BLOG_CONF_PATH
from docs.docs_initializer import new_local_document_set, initialize_docs_dir
from file.blog_config import BlogConfig
from file.file_accessor import read_blog_config, load_category_group_def_yaml
from service.entry_pusher import push_entry_from_docs_to_blog, push_entry_to_docs_and_blog
from service.external.blog_entry_collector import collect_hatena_entry_local_list
from service.local.doc_entry_pusher import push_documents_to_docs
from service.local.doc_entry_retriever import retrieve_document_from_docs, cancel_retrieving_document
from service.local.doc_entry_searcher import search_doc_entry_by_group


def show_hatena_entry(blog_config: BlogConfig, entry_id):
    # for debug
    blog_entry_opt = execute_get_hatena_specified_entry_api(blog_config, entry_id)
    if blog_entry_opt is None:
        print('Nothing')
    print(blog_entry_opt.content)


def main(args: List[str], is_debug: bool):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    category_group_def = load_category_group_def_yaml()

    # show_hatena_entry(blog_config, '26006613443907494')
    # TODO: refactor. use argparse? (no use docopt. because last commit is old)
    # local
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
        if len(args) >= 3 and (args[2] == '-all' or args[2] == '-a'):
            push_entry_to_docs_and_blog(blog_config, category_group_def, target_dirs)
            return
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
        if len(args) >= 3 and (args[2] == '-group' or args[2] == '-g'):
            search_doc_entry_by_group(category_group_def, args[3])
        return
    if len(args) >= 2 and (args[1] == '-delete' or args[1] == '-d'):
        print('Unimplemented')
        return
    # external
    if len(args) >= 2 and (args[1] == '-blog' or args[1] == '-b'):
        if len(args) >= 3 and (args[2] == '-collect' or args[2] == '-c'):
            collect_hatena_entry_local_list(blog_config, category_group_def)
            # put_hatena_summary_page(blog_config, entries_index_map)
            return
        if len(args) >= 3 and (args[2] == '-push' or args[2] == '-p'):
            push_entry_from_docs_to_blog(blog_config, args[3:])
            return


IS_DEBUG = False
main(sys.argv, IS_DEBUG)
