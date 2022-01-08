import codecs
import os
import shutil
from typing import List, Optional

from common.constant import ID_FILE_NAME_HEADER


def make_new_dir(new_dir_path: str):
    os.mkdir(new_dir_path)


def make_new_file(new_file_path: str, write_data: str = ''):
    with codecs.open(new_file_path, mode='w', encoding='utf-8') as f:
        f.write(write_data)


def move_dir(move_from_dir_path: str, move_to_dir_path: str):
    shutil.copytree(move_from_dir_path, move_to_dir_path)
    shutil.rmtree(move_from_dir_path)


def translate_win_files_unusable_char(s: str):
    trans_dict = {
        ':': '：',
        '/': '／',
        '¥': ' ',
        '?': '？',
        '\"': '”',
        '<': '＜',
        '>': '＞',
        '*': '＊',
        '|': '｜',
        ' ': '_'  # Replace to avoid broken links in md files
    }
    return s.translate(str.maketrans(trans_dict))


def get_dir_names_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [d for d in files if os.path.isdir(os.path.join(target_dir_path, d))]


def get_exist_dir_names_in_target_dir(target_dir_path: str, specified_dir_names: List[str]) -> List[str]:
    return [d for d in specified_dir_names if
            os.path.isdir(os.path.join(target_dir_path, d)) and os.path.exists(os.path.join(target_dir_path, d))]


def get_md_file_path_in_target_dir(target_dir_path: str) -> Optional[str]:
    files = os.listdir(target_dir_path)
    extension = '.md'
    for file in files:
        if os.path.isfile(os.path.join(target_dir_path, file)) and file.endswith(extension):
            return target_dir_path + file
    return None
    # files = glob.glob(f'{target_dir_path}/*' + extension)
    # return files[0] if len(files) > 0 else None


def get_file_paths_in_target_dir(target_dir_path: str):
    files = os.listdir(target_dir_path)
    return [target_dir_path + d + '/' for d in files if os.path.isfile(os.path.join(target_dir_path, d))]


def is_exist_file(file_path: str):
    return os.path.exists(file_path) and os.path.isfile(file_path)


def get_id_from_id_file(target_dir_path: str) -> Optional[str]:
    files = os.listdir(target_dir_path)
    for file in files:
        if os.path.isfile(os.path.join(target_dir_path, file)) and file.startswith(ID_FILE_NAME_HEADER):
            return file[len(ID_FILE_NAME_HEADER):]
    return None
