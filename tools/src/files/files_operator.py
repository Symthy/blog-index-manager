import codecs
import os
import shutil
from datetime import datetime
from typing import List


def is_file(target_dir_path: str, file_name: str) -> bool:
    return os.path.isfile(os.path.join(target_dir_path, file_name))


def is_dir(target_dir_path: str) -> bool:
    return os.path.isdir(target_dir_path)


def get_files(target_dir_path: str) -> List[str]:
    return os.listdir(target_dir_path)


def make_new_dir(new_dir_path: str):
    os.mkdir(new_dir_path)


def make_new_file(new_file_path: str, write_data: str = ''):
    with codecs.open(new_file_path, mode='w', encoding='utf-8') as f:
        f.write(write_data)


def copy_dir(target_dir_path: str, copy_to_dir_path: str):
    shutil.copytree(target_dir_path.replace('/', os.sep), copy_to_dir_path.replace('/', os.sep))


def delete_dir(target_dir_path: str):
    shutil.rmtree(target_dir_path)


def delete_file(target_file_path: str):
    os.remove(target_file_path)


def move_dir(move_from_dir_path: str, move_to_dir_path: str):
    copy_dir(move_from_dir_path, move_to_dir_path)
    delete_dir(move_from_dir_path)


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


def is_exist_file(target_dir_path: str):
    return os.path.exists(target_dir_path) and os.path.isfile(target_dir_path)


def is_exist_dir(target_dir_path: str) -> bool:
    return os.path.exists(target_dir_path) and os.path.isdir(target_dir_path)


def get_updated_time_of_target_file(target_file_path) -> datetime:
    # os.stat(target_file_path).st_mtime
    return datetime.fromtimestamp(os.path.getmtime(target_file_path))


# get path
def get_dir_names_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [d for d in files if os.path.isdir(os.path.join(target_dir_path, d))]


def get_exist_dir_names_in_target_dir(target_dir_path: str, specified_dir_names: List[str]) -> List[str]:
    return [d for d in specified_dir_names if
            os.path.isdir(os.path.join(target_dir_path, d)) and os.path.exists(os.path.join(target_dir_path, d))]


def get_file_paths_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [target_dir_path + f for f in files if os.path.isfile(os.path.join(target_dir_path, f))]


def get_file_name_from_file_path(path: str) -> str:
    return path.rsplit('/', 1)[1]


def get_dir_name_from_dir_path(path: str) -> str:
    if path.endswith('/'):
        # dir path: xxx/
        return path[:-1].rsplit('/', 1)[1]
    return path.rsplit('/', 1)[1]
