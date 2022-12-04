from common.constant import BACKUP_DIR_PATH
from domain.doc.doc_entry import DocEntries
from files.files_operator import is_exist_dir, delete_dir


def remove_backup(target_doc_entries: DocEntries):
    for entry in target_doc_entries.entry_list:
        target_dir_path = f'{BACKUP_DIR_PATH}{entry.id}'
        if is_exist_dir(target_dir_path):
            delete_dir(target_dir_path)
