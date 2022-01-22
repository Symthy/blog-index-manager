from typing import List

from common.constant import BACKUP_DIR_PATH, WORK_DIR_PATH, DOCS_DIR_PATH_TEMP_FILE
from docs.doc_entry_list_accessor import is_exist_in_local_entry_list
from docs.docs_grouping_deserializer import deserialize_doc_entry_grouping_data
from domain.doc.doc_entry import DocEntry, new_doc_entry, DocEntries
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import write_text_line, read_file_first_line
from files.files_operator import copy_dir, move_dir, delete_dir, get_dir_name_from_dir_path, \
    resolve_target_entry_dir_path_in_work, delete_file


def retrieve_document_from_docs(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                                category_group_def: CategoryGroupDef, entry_ids: List[str]):
    group_to_categorized_entries = deserialize_doc_entry_grouping_data(category_group_def)
    for doc_entry_id in entry_ids:
        if not is_exist_in_local_entry_list(doc_entry_id):
            print(f'[Error] Nothing specified document (id: {doc_entry_id})')
            return
        target_doc_entry = dump_doc_data_accessor.load_entry(doc_entry_id)
        target_entry_docs_dir_path = target_doc_entry.dir_path
        entry_backup_dir_path = f'{BACKUP_DIR_PATH}{doc_entry_id}/'
        copy_dir(target_entry_docs_dir_path, entry_backup_dir_path)
        print(f'[Info] copy backup (path: {entry_backup_dir_path})')
        write_text_line(f'{entry_backup_dir_path}{DOCS_DIR_PATH_TEMP_FILE}', target_entry_docs_dir_path)
        dir_name = get_dir_name_from_dir_path(target_entry_docs_dir_path)
        move_dir(target_entry_docs_dir_path, f'{WORK_DIR_PATH}{dir_name}/')
        group_to_categorized_entries.remove_entry(category_group_def, target_doc_entry)
    group_to_categorized_entries.dump_docs_data()


def cancel_retrieving_document(category_group_def: CategoryGroupDef, entry_ids: List[str]):
    group_to_categorized_entries = deserialize_doc_entry_grouping_data(category_group_def)
    for doc_entry_id in entry_ids:
        target_dir_path = f'{BACKUP_DIR_PATH}{doc_entry_id}/'
        master_path_temp_file = f'{target_dir_path}{DOCS_DIR_PATH_TEMP_FILE}'
        master_dir_path = read_file_first_line(master_path_temp_file)
        delete_file(master_path_temp_file)
        doc_entry = new_doc_entry(target_dir_path, master_dir_path)
        move_dir(target_dir_path, master_dir_path)
        # delete entry dir during retrieve in work dir
        dir_path_in_work_opt = resolve_target_entry_dir_path_in_work(doc_entry_id)
        if dir_path_in_work_opt is None:
            continue
        delete_dir(dir_path_in_work_opt)
        group_to_categorized_entries.add_entry(category_group_def, doc_entry)
    group_to_categorized_entries.dump_docs_data()
