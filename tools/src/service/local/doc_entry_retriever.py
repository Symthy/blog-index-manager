from typing import List

from common.constant import BACKUP_DIR_PATH, WORK_DIR_PATH
from file.file_accessor import is_exist_in_local_entry_list, get_dir_path_from_local_entry_dump_data, write_text_line, \
    read_file_first_line
from file.files_operator import copy_dir, move_dir, delete_dir, get_dir_name_from_dir_path, resolve_target_dir_in_work

DOCS_DIR_PATH_TEMP_FILE = 'master_path_temp'


def retrieve_document_from_docs(entry_ids: List[str]):
    for doc_entry_id in entry_ids:
        if not is_exist_in_local_entry_list(doc_entry_id):
            print(f'[Error] Nothing specified document (id: {doc_entry_id})')
            return
        target_entry_in_docs_dir_path = get_dir_path_from_local_entry_dump_data(doc_entry_id)
        entry_backup_dir_path = f'{BACKUP_DIR_PATH}{doc_entry_id}/'
        copy_dir(target_entry_in_docs_dir_path, entry_backup_dir_path)
        print(f'[Info] copy backup (path: {entry_backup_dir_path})')
        write_text_line(f'{entry_backup_dir_path}{DOCS_DIR_PATH_TEMP_FILE}', target_entry_in_docs_dir_path)
        dir_name = get_dir_name_from_dir_path(target_entry_in_docs_dir_path)
        move_dir(target_entry_in_docs_dir_path, f'{WORK_DIR_PATH}{dir_name}/')


def cancel_retrieving_document(entry_ids: List[str]):
    for entry_id in entry_ids:
        target_dir_path = f'{BACKUP_DIR_PATH}{entry_id}/'
        master_dir_path = read_file_first_line(f'{target_dir_path}{DOCS_DIR_PATH_TEMP_FILE}')
        move_dir(target_dir_path, master_dir_path)
        dir_path_in_work_opt = resolve_target_dir_in_work(entry_id)
        if dir_path_in_work_opt is None:
            continue
        delete_dir(dir_path_in_work_opt)
