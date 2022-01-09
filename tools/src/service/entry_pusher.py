from typing import List

from common.constant import HATENA_BLOG_ENTRY_LIST_PATH
from domain.blog_entry import BlogEntry, BlogEntries
from domain.doc_entry import DocEntries
from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef
from file.dump.blog_to_doc_mapping import BlogDocEntryMapping
from file.dump.dump_entry_list import DumpEntryList
from file.files_operator import get_md_file_name_in_target_dir
from service.external.blog_entry_pusher import push_hatena_blog_entry
from service.local.doc_entry_pusher import push_documents_to_docs


def __push_entry_from_docs_to_blog(blog_config: BlogConfig, doc_entries: DocEntries):
    blog_doc_mapping = BlogDocEntryMapping()
    dump_blog_entry_list = DumpEntryList(HATENA_BLOG_ENTRY_LIST_PATH)
    blog_entries: List[BlogEntry] = []
    for doc_entry in doc_entries.entry_list:
        blog_entry_id_opt = blog_doc_mapping.get_blog_entry_id(doc_entry.id)
        md_file_name_opt = get_md_file_name_in_target_dir(doc_entry.dir_path)
        if md_file_name_opt is None:
            # don't happen. to make sure
            continue
        blog_entry_opt = push_hatena_blog_entry(blog_config, doc_entry.dir_path, md_file_name_opt, doc_entry.title,
                                                doc_entry.top_category, blog_entry_id_opt)
        if blog_entry_opt is None:
            print(f'[Info] blog push skip. (dir: {doc_entry.dir_path})')
            continue
        blog_entries.append(blog_entry_opt)
        dump_blog_entry_list.push_entry(blog_entry_opt)
        blog_doc_mapping.push_entry_pair(blog_entry_opt.id, doc_entry.id)
    # dump to file
    BlogEntries(blog_entries).dump_all_data()
    dump_blog_entry_list.dump_file()
    blog_doc_mapping.dump_file()
    # Todo: update_blog_entry_index(category_group_def, blog_entries)


def push_entry_to_docs_and_blog(blog_config: BlogConfig, category_group_def: CategoryGroupDef,
                                target_dir_names: List[str] = None):
    doc_entries = push_documents_to_docs(category_group_def, target_dir_names)
    __push_entry_from_docs_to_blog(blog_config, doc_entries)


def push_entry_from_docs_to_blog(blog_config: BlogConfig, target_doc_entry_ids: List[str]):
    doc_entries = DocEntries.init_by_entry_ids(target_doc_entry_ids)
    __push_entry_from_docs_to_blog(blog_config, doc_entries)
