from typing import List, Optional

from docs.doc_entry_factory import build_doc_entries
from docs.docs_backuper import DocsBackuper
from docs.docs_movers import resolve_moving_from_and_to_dir_path, move_documents_to_docs_dir
from docs.docs_writer import save_doc_entries
from domain.doc.doc_entry import DocEntries, DocEntry
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from service.entry_summary_factory import EntrySummaryFactory
from service.local.doc_entry_summary_updater import update_doc_entry_summary_file


def push_documents_to_docs(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                           category_group_def: CategoryGroupDef, entry_summary_factory: EntrySummaryFactory,
                           docs_backuper: DocsBackuper,
                           is_pickup: bool, target_dir_names: List[str] = None) -> Optional[DocEntries]:
    moving_from_and_to_path_dict = resolve_moving_from_and_to_dir_path(category_group_def, target_dir_names)
    if len(moving_from_and_to_path_dict) == 0:
        return None
    # Todo: specifiable entry id
    # Todo: validate dir name
    new_doc_entries = build_doc_entries(dump_doc_data_accessor, moving_from_and_to_path_dict, is_pickup)
    docs_backuper.remove_backup_doc_entries(new_doc_entries)

    save_doc_entries(dump_doc_data_accessor, category_group_def, new_doc_entries)
    update_doc_entry_summary_file(entry_summary_factory)
    move_documents_to_docs_dir(moving_from_and_to_path_dict)
    return new_doc_entries
