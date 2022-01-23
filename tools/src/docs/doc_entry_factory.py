from datetime import datetime
from typing import Optional, Dict

from common.constant import ID_FILE_NAME_HEADER, CATEGORY_FILE_NAME
from docs.doc_set_accessor import get_md_file_path_in_target_dir, get_doc_title_from_md_file, get_id_from_id_file
from domain.doc.doc_entry import DocEntry, DocEntries
from dump.interface import IDumpEntriesAccessor
from files.file_accessor import write_text_line, read_text_file
from files.files_operator import get_dir_name_from_dir_path, get_file_name_from_file_path
from ltime.time_resolver import get_current_datetime, convert_datetime_to_time_sequence


def new_doc_entries(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                    move_from_path_to_move_to_path_dict: Dict[str, str]) -> DocEntries:
    docs_entry_list = []
    for move_from_path, move_to_path in move_from_path_to_move_to_path_dict.items():
        docs_entry_opt = new_doc_entry(dump_doc_data_accessor, move_from_path, move_to_path)
        if docs_entry_opt is not None:
            docs_entry_list.append(docs_entry_opt)
    return DocEntries(docs_entry_list)


def new_doc_entry(dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry], target_dir_path: str,
                  move_to_path: str) -> Optional[DocEntry]:
    created_datetime: datetime = get_current_datetime()
    md_file_path: Optional[str] = get_md_file_path_in_target_dir(target_dir_path)
    dir_name = get_dir_name_from_dir_path(target_dir_path)
    if md_file_path is None:
        print(f'[Error] skip: non exist md file (dir: {dir_name})')
        return None
    doc_title = get_doc_title_from_md_file(md_file_path)
    if doc_title is None:
        print(f'[Error] skip: empty doc title (dir: {dir_name})')
        return None
    entry_id: Optional[str] = get_id_from_id_file(target_dir_path)
    if entry_id is None:
        entry_id = convert_datetime_to_time_sequence(created_datetime)
        id_file_path = f'{target_dir_path}/{ID_FILE_NAME_HEADER}{entry_id}'
        write_text_line(id_file_path, entry_id)
    doc_file_name = get_file_name_from_file_path(md_file_path)
    categories = read_text_file(target_dir_path + CATEGORY_FILE_NAME)
    created_at = created_datetime
    updated_at = None
    if dump_doc_data_accessor.has_entry(entry_id):
        created_at = None  # use existed time in dump file
        updated_at = get_current_datetime()
    return DocEntry(entry_id, doc_title, move_to_path, doc_file_name, categories, created_at, updated_at)
