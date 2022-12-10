from typing import List

from blogs.blog_grouping_deserializer import deserialize_grouping_blog_entries
from blogs.dump_blog_entries_accessor import DumpBlogEntriesAccessor
from blogs.hatena.blog_api_executor import HatenaBlogApiExecutor
from common.constant import BLOG_CONF_PATH
from docs.docs_backuper import DocsBackuper
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from docs.docs_mover import DocsMover
from docs.dump_doc_entries_accessor import DumpDocEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import read_blog_config, read_md_file
from files.md_data_handler import replace_image_link_in_md_data
from main import show_hatena_blog_entry, show_hatena_photo_entry
from oauth.oauth import execute_oauth, get_hatena_bookmarks
from service.entry_pusher import push_entry_from_docs_to_blog, push_entry_to_docs_and_blog
from service.entry_summary_factory import EntrySummaryFactory
from service.external.blog_entry_collector import collect_hatena_entry_local_list
from service.external.blog_entry_pusher import push_photo_entries, push_blog_entry
from service.external.blog_entry_summary_updater import update_blog_entry_summary_file, put_hatena_summary_page
from service.local.doc_entry_generator import new_local_document_set
from service.local.doc_entry_pusher import DocEntryPusher
from service.local.doc_entry_retriever import DocEntryRetriever
from service.local.doc_entry_searcher import search_doc_entry_by_group, search_doc_entry_by_category, \
    search_doc_entry_by_title
from service.local.doc_entry_summary_writer import DocEntrySummaryWriter
from service.local.doc_entry_updater import DocEntryUpdater
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
  -d, --docs <OPTS>
    OPTS (can't also specify the following together):
      -pu, --pickup <DocEntryID>            toggle on/off of pickup in specified entry.                
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
    dump_blog_entries_accessor = DumpBlogEntriesAccessor()
    dump_doc_entries_accessor = DumpDocEntriesAccessor()
    category_group_def = CategoryGroupDef.load_category_group_def_yaml()
    grouping_doc_entries_deserializer = DocsGroupingDataDeserializer(dump_doc_entries_accessor, category_group_def)
    entry_summary_factory = EntrySummaryFactory(dump_doc_entries_accessor, dump_blog_entries_accessor,
                                                category_group_def, grouping_doc_entries_deserializer)
    doc_entry_summary_writer = DocEntrySummaryWriter(entry_summary_factory)
    docs_backuper = DocsBackuper()

    # TODO: refactor and add validation. use argparse (no use docopt. because last commit is old)
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
        docs_mover = DocsMover(category_group_def)
        doc_entry_pusher = DocEntryPusher(dump_doc_entries_accessor, category_group_def, doc_entry_summary_writer,
                                          docs_backuper, docs_mover, grouping_doc_entries_deserializer)
        if len(args) >= 3 and (args[2] == '--all' or args[2] == '-a'):
            ex_opts: List[str] = args[3:]
            is_draft = True if len(ex_opts) >= 1 and ('--draft' in ex_opts or '-d' in ex_opts) else False
            is_title_escape = True if len(ex_opts) >= 1 and ('--title-escape' in ex_opts or '-te' in ex_opts) else False
            is_pickup = True if len(ex_opts) >= 1 and ('--pickup' in ex_opts or '-pu' in ex_opts) else False
            push_entry_to_docs_and_blog(api_executor, dump_blog_entries_accessor, entry_summary_factory,
                                        doc_entry_pusher, is_draft, is_title_escape, is_pickup, target_dirs)
            print('[Info] Success: pushed document to docs dir and blog.')
            return
        ex_opts: List[str] = args[2:]
        is_pickup = True if len(ex_opts) >= 1 and ('--pickup' in ex_opts or '-pu' in ex_opts) else False
        result = doc_entry_pusher.execute(is_pickup, target_dirs)
        if result is None:
            print('[Warn] Non-exist specified document in work dir.')
        else:
            print('[Info] Success: pushed document to docs dir.')
        return
    if len(args) >= 2 and (args[1] == '--retrieve' or args[1] == '-r'):
        doc_entry_retriever = DocEntryRetriever(dump_doc_entries_accessor, docs_backuper,
                                                grouping_doc_entries_deserializer)
        if len(args) >= 3 and (args[2] == '--cancel' or args[2] == '-c'):
            doc_entry_retriever.cancel_retrieving_document(args[3:])
            print('[Info] Success: retrieve cancel.')
        else:
            doc_entry_retriever.retrieve_document_from_docs(args[2:])
            print('[Info] Success: retrieve document to work dir.')
        return
    if len(args) >= 2 and (args[1] == '--search' or args[1] == '-s'):
        if len(args) >= 3 and (args[2] == '--group' or args[2] == '-g'):
            search_doc_entry_by_group(category_group_def, grouping_doc_entries_deserializer, args[3])
            return
        if len(args) >= 3 and (args[2] == '--category' or args[2] == '-c'):
            search_doc_entry_by_category(category_group_def, grouping_doc_entries_deserializer, args[3])
            return
        if len(args) >= 3 and (args[2] == '--title' or args[2] == '-t'):
            search_doc_entry_by_title(dump_doc_entries_accessor, category_group_def, args[3])
            return
        search_doc_entry_by_title(dump_doc_entries_accessor, category_group_def, args[2])
        return
    if len(args) >= 2 and (args[1] == '--delete' or args[1] == '-d'):
        print('[Error] Unimplemented')
        return
    if len(args) >= 2 and (args[1] == '--organize' or args[1] == '-o'):
        print('[Error] Unimplemented')
        return

    # local
    if len(args) >= 2 and (args[1] == '--docs' or args == '-d'):
        doc_entry_updater = DocEntryUpdater(dump_doc_entries_accessor, doc_entry_summary_writer)
        if len(args) >= 3 and (args[2] == '--pickup' or args[2] == '-pu'):
            doc_entry_updater.update_pickup()

    # external
    if len(args) >= 2 and (args[1] == '--blog' or args[1] == '-b'):
        if len(args) >= 3 and (args[2] == '--push' or args[2] == '-p'):
            ex_opts: List[str] = args[3:]
            is_draft = True if len(ex_opts) >= 1 and ('--draft' in ex_opts or '-d' in ex_opts) else False
            is_title_escape = True if len(ex_opts) >= 1 and ('--title-escape' in ex_opts or '-te' in ex_opts) else False
            push_entry_from_docs_to_blog(api_executor, dump_blog_entries_accessor, dump_doc_entries_accessor,
                                         entry_summary_factory, args[3:], is_draft, is_title_escape)
            print('[Info] Success: pushed specified document to blog.')
            return
        if len(args) >= 3 and (args[2] == '--summary' or args[2] == '-s'):
            is_success = put_hatena_summary_page(api_executor, entry_summary_factory)
            if is_success:
                print('[Info] Success: blog summary page updated')
            else:
                print('[Error] Failure: blog summary page updated')
            return
    if len(args) >= 2 and (args[1] == '--blog-collect' or args[2] == '-bc'):
        collect_hatena_entry_local_list(api_executor, dump_blog_entries_accessor, entry_summary_factory)
        print('[Info] Success: blog entries collection')
        return

    # hidden option. for testing
    if len(args) >= 2 and args[1] == '--wsse':
        print(api_executor.build_request_header())
        return
    if len(args) >= 2 and args[1] == '--update-summary':
        update_blog_entry_summary_file(entry_summary_factory)
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
        print(deserialize_grouping_blog_entries(dump_blog_entries_accessor, category_group_def).convert_md_lines())
        return
    if len(args) >= 3 and args[1] == '--put-photo':
        doc_id = args[2]
        result = push_photo_entries(blog_config, dump_doc_entries_accessor.load_entry(doc_id))
        print(result.build_dump_data())
        return
    if len(args) >= 3 and args[1] == '--put-blog':
        doc_id = args[2]
        result = push_blog_entry(blog_config, dump_doc_entries_accessor.load_entry(doc_id), False, False)
        print(result.build_dump_data())
        return
    if len(args) >= 2 and args[1] == '--replace-md':
        md_data = read_md_file('./docs/Program/Golang/Golang_Generics/doc.md')
        blog_entry_id = '13574176438053271362'
        blog_entry = dump_blog_entries_accessor.load_entry(blog_entry_id)
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
