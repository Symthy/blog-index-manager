from typing import List

from blogs.blog_grouping_deserializer import deserialize_blog_entry_grouping_data
from blogs.dump_blog_entries_accessor import DumpBlogEntriesAccessor
from blogs.hatena.blog_api_executor import HatenaBlogApiExecutor
from common.constant import BLOG_CONF_PATH
from docs.dump_doc_entries_accessor import DumpDocEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import read_blog_config, read_md_file
from files.md_data_handler import replace_image_link_in_md_data
from main import show_hatena_blog_entry, show_hatena_photo_entry
from oauth.oauth import execute_oauth, get_hatena_bookmarks
from service.entry_pusher import push_entry_from_docs_to_blog, push_entry_to_docs_and_blog
from service.external.blog_entry_collector import collect_hatena_entry_local_list
from service.external.blog_entry_index_updater import update_blog_entry_summary_file
from service.external.blog_entry_pusher import put_hatena_summary_page, push_photo_entries, push_blog_entry
from service.local.doc_entry_generator import new_local_document_set
from service.local.doc_entry_pusher import push_documents_to_docs
from service.local.doc_entry_retriever import retrieve_document_from_docs, cancel_retrieving_document
from service.local.doc_entry_searcher import search_doc_entry_by_group, search_doc_entry_by_category, \
    search_doc_entry_by_title
from service.local.docs_initializer import initialize_docs_dir

USAGE_CONTENT = """Document and Blog Entry Manager

USAGE:
  <command> [OPTIONS]

OPTIONS:
  -i, --init                            initialize docs directory (don't delete exist file and dir).
  -n, --new [<OPTS>]                    new document set under "work" dir (create dir, md file and category file).
    OPTS (can also specify the following together):                                
      -t, --title <DocTitle>                specified document title (default: "doc").
      -c, --category <CategoryName>         specified category (default: empty value).
  -s, --search <OPTS>                   search document entry (show entry id, title, group, category).
    OPTS:
      -g, --group <Group Name>              search by group name.
      -c, --category <Category Name>        search by category name.
      -t, --title <Keyword>                 search by title keyword (partial match). 
  -p, --push [<OPTS>] <DirName>         push document set from "work" dir to "docs" dir.
    OPTS: 
      -a, --all                         in addition to the above, post your blog.
      -d, --draft                       post as draft entry.
      -pu,--pickup                      post as pickup entry.
      -te,--title-escape                escape the entry title.
  -r, --retrieve [<OPTS>] <DocEntryID>  retrieve document set from "docs" dir to "work" dir (and backup).
    OPTS: 
      -c, --cancel                      cancel retrieve (move the backup back to "docs" dir).
  -b, --blog <OPTS>                     operation to your blog.
    OPTS (can't also specify the following together):                                
      -p, --push <DocEntryID>               post specified document to your blog.
      -d, --draft                       post as draft entry.
      -pu,--pickup                      post as pickup entry.
      -te,--title-escape                escape the entry title.
  -bc,--blog-collect                    collect all blog entries from your blog. (experimental function)
  -h, --help                            show usage.
"""


def print_usage():
    print(USAGE_CONTENT)


def execute_command(args: List[str]):
    blog_config = read_blog_config(BLOG_CONF_PATH)
    api_executor = HatenaBlogApiExecutor(blog_config)
    dump_blog_data_accessor = DumpBlogEntriesAccessor()
    dump_doc_data_accessor = DumpDocEntriesAccessor()
    category_group_def = CategoryGroupDef.load_category_group_def_yaml()

    # TODO: refactor and add validation. use argparse? (no use docopt. because last commit is old)
    # local
    if len(args) >= 2 and (args[1] == '--init' or args[1] == '-i'):
        initialize_docs_dir(category_group_def)
        print('[Info] Success: created \"docs\" dir')
        return
    if len(args) >= 2 and (args[1] == '--new' or args[1] == '-n'):
        created_dir_name_opt = new_local_document_set(args)
        if created_dir_name_opt is not None:
            print(f'[Info] Success: created \"{created_dir_name_opt}\" dir in work dir')
        return
    if len(args) >= 2 and (args[1] == '--push' or args[1] == '-p'):
        target_dirs = args[2:] if len(args) > 2 else []
        if len(args) >= 3 and (args[2] == '--all' or args[2] == '-a'):
            ex_opts: List[str] = args[3:]
            is_draft = True if len(ex_opts) >= 1 and ('--draft' in ex_opts or '-d' in ex_opts) else False
            is_title_escape = True if len(ex_opts) >= 1 and ('--title-escape' in ex_opts or '-te' in ex_opts) else False
            is_pickup = True if len(ex_opts) >= 1 and ('--pickup' in ex_opts or '-pu' in ex_opts) else False
            push_entry_to_docs_and_blog(api_executor, dump_blog_data_accessor, dump_doc_data_accessor,
                                        category_group_def, is_draft, is_title_escape, target_dirs)
            print('[Info] Success: pushed document to docs dir and blog.')
            return
        result = push_documents_to_docs(dump_doc_data_accessor, category_group_def, target_dirs)
        if result is None:
            print('[Warn] Non-exist specified document in work dir.')
        else:
            print('[Info] Success: pushed document to docs dir.')
        return
    if len(args) >= 2 and (args[1] == '--retrieve' or args[1] == '-r'):
        if len(args) >= 3 and (args[2] == '--cancel' or args[2] == '-c'):
            cancel_retrieving_document(dump_doc_data_accessor, category_group_def, args[3:])
            print('[Info] Success: retrieve cancel.')
        else:
            retrieve_document_from_docs(dump_doc_data_accessor, category_group_def, args[2:])
            print('[Info] Success: retrieve document to work dir.')
        return
    if len(args) >= 2 and (args[1] == '--search' or args[1] == '-s'):
        if len(args) >= 3 and (args[2] == '--group' or args[2] == '-g'):
            search_doc_entry_by_group(category_group_def, args[3])
            return
        if len(args) >= 3 and (args[2] == '--category' or args[2] == '-c'):
            search_doc_entry_by_category(category_group_def, args[3])
            return
        if len(args) >= 3 and (args[2] == '--title' or args[2] == '-t'):
            search_doc_entry_by_title(dump_doc_data_accessor, category_group_def, args[3])
            return
        search_doc_entry_by_title(dump_doc_data_accessor, category_group_def, args[2])
        return
    if len(args) >= 2 and (args[1] == '--delete' or args[1] == '-d'):
        print('[Error] Unimplemented')
        return
    if len(args) >= 2 and (args[1] == '--organize' or args[1] == '-o'):
        print('[Error] Unimplemented')
        return

    # external
    if len(args) >= 2 and (args[1] == '--blog' or args[1] == '-b'):
        if len(args) >= 3 and (args[2] == '--push' or args[2] == '-p'):
            ex_opts: List[str] = args[3:]
            is_draft = True if len(ex_opts) >= 1 and ('--draft' in ex_opts or '-d' in ex_opts) else False
            is_title_escape = True if len(ex_opts) >= 1 and ('--title-escape' in ex_opts or '-te' in ex_opts) else False
            is_pickup = True if len(ex_opts) >= 1 and ('--pickup' in ex_opts or '-pu' in ex_opts) else False
            push_entry_from_docs_to_blog(api_executor, dump_blog_data_accessor, dump_doc_data_accessor,
                                         category_group_def, args[3:], is_draft, is_title_escape)
            print('[Info] Success: pushed specified document to blog.')
            return
        if len(args) >= 3 and (args[2] == '--summary' or args[2] == '-s'):
            is_success = put_hatena_summary_page(api_executor, category_group_def)
            if is_success:
                print('[Info] Success: blog summary page updated')
            else:
                print('[Error] Failure: blog summary page updated')
            return
    if len(args) >= 2 and (args[1] == '--blog-collect' or args[2] == '-bc'):
        collect_hatena_entry_local_list(api_executor, dump_blog_data_accessor, category_group_def)
        print('[Info] Success: blog entries collection')
        return

    # hidden option. for testing
    if len(args) >= 2 and args[1] == '--wsse':
        print(api_executor.build_request_header())
        return
    if len(args) >= 2 and args[1] == '--update-summary':
        update_blog_entry_summary_file(dump_blog_data_accessor, category_group_def)
        return
    if len(args) >= 3 and args[1] == '--get-blog':
        hatena_blog_entry_id = args[2]
        show_hatena_blog_entry(blog_config, hatena_blog_entry_id)
        return
    if len(args) >= 3 and args[1] == '--get-photo':
        hatena_photo_entry_id = args[2]
        show_hatena_photo_entry(blog_config, hatena_photo_entry_id)
        return
    if len(args) >= 2 and args[1] == '--show-blog-summary':
        print(deserialize_blog_entry_grouping_data(category_group_def).convert_md_lines())
        return
    if len(args) >= 3 and args[1] == '--put-photo':
        doc_id = args[2]
        result = push_photo_entries(blog_config, dump_doc_data_accessor.load_entry(doc_id))
        print(result.build_dump_data())
        return
    if len(args) >= 3 and args[1] == '--put-blog':
        doc_id = args[2]
        result = push_blog_entry(blog_config, dump_doc_data_accessor.load_entry(doc_id), False, False)
        print(result.build_dump_data())
        return
    if len(args) >= 2 and args[1] == '--replace-md':
        md_data = read_md_file('./docs/Program/Golang/Golang_Generics/doc.md')
        blog_entry_id = '13574176438053271362'
        blog_entry = dump_blog_data_accessor.load_entry(blog_entry_id)
        print(replace_image_link_in_md_data(md_data, blog_entry.doc_images))
        return
    if len(args) >= 2 and args[1] == '--oauth':
        execute_oauth(blog_config)
        return
    if len(args) >= 2 and args[1] == '--bookmarks':
        get_hatena_bookmarks(blog_config)
        return

    # usage
    if len(args) >= 2 and (args[1] == '--help' or args[1] == '-h'):
        print_usage()
        return
    print_usage()
