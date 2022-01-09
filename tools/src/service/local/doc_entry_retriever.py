from typing import List

from common.constant import BACKUP_DIR_PATH, WORK_DIR_PATH
from file.file_accessor import is_exist_in_local_entry_list, get_dir_path_from_local_entry_dump_data, write_text_line, \
    read_file_first_line
from file.files_operator import copy_dir, move_dir, get_files_name_from_path, delete_dir

DOCS_DIR_PATH_TEMP_FILE = 'master_path_temp'


def retrieve_document_from_docs(entry_ids: List[str]):
    for entry_id in entry_ids:
        if not is_exist_in_local_entry_list(entry_id):
            print(f'[Error] Nothing specified document (id: {entry_id})')
            return
        target_entry_in_docs_dir_path = get_dir_path_from_local_entry_dump_data(entry_id)
        entry_backup_dir_path = f'{BACKUP_DIR_PATH}{entry_id}/'
        copy_dir(target_entry_in_docs_dir_path, entry_backup_dir_path)
        print(f'[Info] copy backup (path: {entry_backup_dir_path})')
        write_text_line(f'{entry_backup_dir_path}{DOCS_DIR_PATH_TEMP_FILE}', target_entry_in_docs_dir_path)
        dir_name = get_files_name_from_path(target_entry_in_docs_dir_path)
        move_dir(target_entry_in_docs_dir_path, f'{WORK_DIR_PATH}{dir_name}/')


def cancel_retrieving_document(entry_ids: List[str]):
    for entry_id in entry_ids:
        target_dir_path = f'{BACKUP_DIR_PATH}{entry_id}/'
        master_dir_path = read_file_first_line(f'{target_dir_path}{DOCS_DIR_PATH_TEMP_FILE}')
        move_dir(target_dir_path, master_dir_path)
        delete_dir(f'{WORK_DIR_PATH}{entry_id}/')
