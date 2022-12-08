from typing import List

from blogs.api.interface import IBlogApiExecutor
from docs.docs_backuper import DocsBackuper
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from domain.blog.blog_entry import BlogEntry, BlogEntries
from domain.doc.doc_entry import DocEntries, DocEntry
from dump.blog_to_doc_mapping import BlogDocEntryMapping
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from service.entry_summary_factory import EntrySummaryFactory
from service.external.blog_entry_pusher import push_blog_and_photo_entry
from service.external.blog_entry_summary_updater import update_blog_entry_summary_file
from service.local.doc_entry_pusher import push_documents_to_docs
from service.local.doc_entry_summary_writer import DocEntrySummaryWriter


# Todo: classify
def push_entry_to_docs_and_blog(api_executor: IBlogApiExecutor,
                                dump_blog_data_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
                                dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                                category_group_def: CategoryGroupDef,
                                entry_summary_factory: EntrySummaryFactory,
                                doc_entry_summary_writer: DocEntrySummaryWriter,
                                docs_backuper: DocsBackuper,
                                grouping_doc_entries_deserializer: DocsGroupingDataDeserializer,
                                is_draft: bool, is_title_escape: bool, is_pickup: bool,
                                target_dir_names: List[str] = None):
    new_doc_entries = push_documents_to_docs(dump_doc_data_accessor, category_group_def, doc_entry_summary_writer,
                                             docs_backuper, grouping_doc_entries_deserializer, is_pickup,
                                             target_dir_names)
    if new_doc_entries is None:
        return
    __push_entry_from_docs_to_blog(api_executor, dump_blog_data_accessor, entry_summary_factory,
                                   new_doc_entries, is_draft, is_title_escape)


def push_entry_from_docs_to_blog(api_executor: IBlogApiExecutor,
                                 dump_blog_data_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
                                 dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                                 entry_summary_factory: EntrySummaryFactory, target_doc_entry_ids: List[str],
                                 is_draft: bool = False, is_title_escape: bool = False):
    target_doc_entries: DocEntries = dump_doc_data_accessor.load_entries(target_doc_entry_ids)
    __push_entry_from_docs_to_blog(api_executor, dump_blog_data_accessor, entry_summary_factory,
                                   target_doc_entries, is_draft, is_title_escape)


def __push_entry_from_docs_to_blog(api_executor: IBlogApiExecutor,
                                   dump_blog_data_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
                                   entry_summary_factory: EntrySummaryFactory,
                                   doc_entries: DocEntries, is_draft: bool, is_title_escape: bool):
    blog_doc_mapping = BlogDocEntryMapping()
    updated_blog_entry_list: List[BlogEntry] = []
    for doc_entry in doc_entries.entry_list:
        blog_entry_id_opt = blog_doc_mapping.get_blog_entry_id(doc_entry.id)
        old_blog_entry_opt = None if blog_entry_id_opt is None else dump_blog_data_accessor.load_entry(
            blog_entry_id_opt)
        new_blog_entry_opt = push_blog_and_photo_entry(api_executor, doc_entry, is_draft, is_title_escape,
                                                       old_blog_entry_opt)
        if new_blog_entry_opt is None:
            print(f'[Info] blog push skip. (dir: {doc_entry.dir_path})')
            continue
        updated_blog_entry_list.append(new_blog_entry_opt)
        blog_doc_mapping.push_entry_pair(new_blog_entry_opt.id, doc_entry.id)
    # dump to file
    updated_blog_entries = BlogEntries(updated_blog_entry_list)
    dump_blog_data_accessor.save_entries(updated_blog_entries)
    blog_doc_mapping.dump_file()
    update_blog_entry_summary_file(entry_summary_factory)
