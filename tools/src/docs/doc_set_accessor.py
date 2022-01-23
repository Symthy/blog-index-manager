import os
from typing import Optional, List

from common.constant import ID_FILE_NAME_HEADER, WORK_DIR_PATH
from files.file_accessor import read_file_first_line
from files.files_operator import get_file_paths_in_target_dir, is_file, get_files, is_dir


def get_doc_title_from_md_file(doc_md_file_path: str) -> Optional[str]:
    doc_title = read_file_first_line(doc_md_file_path)
    if len(doc_title) == 0:
        return None
    return doc_title


def get_id_from_id_file(target_dir_path: str) -> Optional[str]:
    files = get_files(target_dir_path)
    for files_name in files:
        if is_file(target_dir_path, files_name) and files_name.startswith(ID_FILE_NAME_HEADER):
            return files_name[len(ID_FILE_NAME_HEADER):]
    return None


def get_md_file_name_in_target_dir(target_dir_path: str) -> Optional[str]:
    files = get_files(target_dir_path)
    extension = '.md'
    for file in files:
        if is_file(target_dir_path, file) and file.endswith(extension):
            return file
    return None


def resolve_target_entry_dir_path_in_work(entry_id: str) -> Optional[str]:
    return __resolve_target_entry_dir_path(WORK_DIR_PATH, entry_id)


def __resolve_target_entry_dir_path(target_dir_path: str, entry_id: str) -> Optional[str]:
    files = os.listdir(target_dir_path)
    for dir_name in files:
        dir_path = f'{target_dir_path}{dir_name}'
        if not is_dir(dir_path):
            continue
        id_opt = get_id_from_id_file(dir_path)
        if entry_id == id_opt:
            return dir_path
    return None


def get_md_file_path_in_target_dir(target_dir_path: str) -> Optional[str]:
    me_file_name_opt = get_md_file_name_in_target_dir(target_dir_path)
    return target_dir_path + me_file_name_opt if me_file_name_opt is not None else None
    # files = glob.glob(f'{target_dir_path}/*' + extension)
    # return files[0] if len(files) > 0 else None


def get_image_file_paths_in_target_dir(target_dir_path: str) -> List[str]:
    # Todo: refactor
    file_paths = get_file_paths_in_target_dir(target_dir_path)
    image_file_paths = []
    for file_path in file_paths:
        if file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.bmp') or \
                file_path.endswith('.svg'):
            image_file_paths.append(file_path)
    return image_file_paths
