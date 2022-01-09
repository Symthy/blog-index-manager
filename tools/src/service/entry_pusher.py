from typing import List

from domain.doc_entry import DocEntries
from file.blog_config import BlogConfig
from file.blog_to_doc_mapping import BlogDocMapping
from file.category_group_def import CategoryGroupDef
from file.files_operator import get_md_file_name_in_target_dir
from service.external.blog_entry_updater import push_hatena_blog_entry
from service.local.doc_entry_pusher import push_documents_to_docs


def __push_entry_from_docs_to_blog(blog_config: BlogConfig, doc_entries: DocEntries):
    blog_doc_mapping = BlogDocMapping()
    for doc_entry in doc_entries.entry_list:
        blog_entry_id_opt = blog_doc_mapping.get_blog_entry_id(doc_entry.id)
        md_file_name_opt = get_md_file_name_in_target_dir(doc_entry.dir_path)
        if md_file_name_opt is None:
            continue
        push_hatena_blog_entry(blog_config, doc_entry.dir_path, md_file_name_opt, doc_entry.title,
                               doc_entry.top_category, blog_entry_id_opt)


def push_entry_to_docs_and_blog(blog_config: BlogConfig, category_group_def: CategoryGroupDef,
                                target_dir_names: List[str] = None):
    doc_entries = push_documents_to_docs(category_group_def, target_dir_names)
    __push_entry_from_docs_to_blog(blog_config, doc_entries)


def push_entry_from_docs_to_blog(blog_config: BlogConfig, target_doc_entry_ids: List[str]):
    doc_entries = DocEntries.init_by_entry_ids(target_doc_entry_ids)
    __push_entry_from_docs_to_blog(blog_config, doc_entries)
