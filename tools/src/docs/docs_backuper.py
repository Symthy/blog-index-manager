from common.constant import BACKUP_DIR_PATH, WORK_DIR_PATH, DOCS_DIR_PATH_TEMP_FILE
from docs.doc_set_accessor import resolve_entry_dir_path_in_work
from domain.doc.doc_entry import DocEntries, DocEntry
from files.file_accessor import write_text_line, read_file_first_line
from files.files_operator import is_exist_dir, delete_dir, copy_dir, get_dir_name_from_dir_path, move_dir, delete_file


class DocsBackuper:

    def __init__(self, backup_dir_path=None):
        if backup_dir_path is None:
            self.backup_dir_path = BACKUP_DIR_PATH
            return
        self.backup_dir_path = backup_dir_path

    def resolve_backup_entry_dir_path(self, doc_entry_id: str):
        return f'{self.backup_dir_path}{doc_entry_id}/'

    def remove_backup_doc_entries(self, doc_entries: DocEntries):
        for entry in doc_entries.entry_list:
            self.__remove_backup_doc_entries(entry)

    def __remove_backup_doc_entries(self, doc_entry: DocEntry):
        target_dir_path = f'{self.backup_dir_path}{doc_entry.id}'
        if is_exist_dir(target_dir_path):
            delete_dir(target_dir_path)

    def sava_backup_doc_entry(self, doc_entry: DocEntry):
        entry_backup_dir_path = self.resolve_backup_entry_dir_path(doc_entry.id)
        copy_dir(doc_entry.dir_path, entry_backup_dir_path)
        print(f'[Info] copy backup (path: {entry_backup_dir_path})')
        write_text_line(f'{entry_backup_dir_path}{DOCS_DIR_PATH_TEMP_FILE}', doc_entry.dir_path)
        dir_name = get_dir_name_from_dir_path(doc_entry.dir_path)
        move_dir(doc_entry.dir_path, f'{WORK_DIR_PATH}{dir_name}/')

    def retrieve_backup_doc_entry(self, doc_entry_id: str):
        backup_entry_dir_path = self.resolve_backup_entry_dir_path(doc_entry_id)
        master_path_temp_file = f'{backup_entry_dir_path}{DOCS_DIR_PATH_TEMP_FILE}'
        master_entry_dir_path = read_file_first_line(master_path_temp_file)
        delete_file(master_path_temp_file)
        move_dir(backup_entry_dir_path, master_entry_dir_path)
        # delete entry dir during retrieve in work dir
        dir_path_in_work_opt = resolve_entry_dir_path_in_work(doc_entry_id)
        if dir_path_in_work_opt is None:
            return
        delete_dir(dir_path_in_work_opt)
