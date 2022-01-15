import os
from typing import List, Optional, Dict

from common.constant import NON_CATEGORY_GROUP_NAME, WORK_DIR_PATH, DOCS_DIR_PATH, CATEGORY_FILE_NAME
from file.category_group_def import CategoryGroupDef
from file.file_accessor import read_text_file, get_doc_title_from_md_file
from file.files_operator import get_dir_names_in_target_dir, get_exist_dir_names_in_target_dir, \
    get_md_file_path_in_target_dir, translate_win_files_unusable_char, move_dir


def move_documents_to_docs_dir(move_from_to_path_dict: Dict[str, str]):
    for move_from_dir_path, move_to_dir_path in move_from_to_path_dict.items():
        move_dir(move_from_dir_path, move_to_dir_path)


def resolve_move_from_and_move_to_dir_path_dict(category_group_def: CategoryGroupDef, target_dir_names: List[str]) \
        -> Dict[str, str]:
    # return: key:move_from_path value: move_to_path
    target_dir_path_to_name_dict = __resolve_target_dir_names(target_dir_names)
    path_dict = {}
    for move_from_dir_path in target_dir_path_to_name_dict:
        md_file_path: Optional[str] = get_md_file_path_in_target_dir(move_from_dir_path)
        if md_file_path is None:
            # skip when non exist md file in target dir
            print(f'[Info] skip move dir: non exist md file (dir: {target_dir_path_to_name_dict[move_from_dir_path]})')
            continue
        doc_title: Optional[str] = get_doc_title_from_md_file(md_file_path)
        if doc_title is None:
            print(f'[Warn] empty doc title (dir: {target_dir_path_to_name_dict[move_from_dir_path]})')
            continue
        move_to_dir_path = __resolve_move_to_dir_name_and_path(category_group_def, move_from_dir_path, doc_title)
        path_dict[move_from_dir_path] = move_to_dir_path
    return path_dict


def __resolve_move_to_dir_name_and_path(category_group_def: CategoryGroupDef, move_from_dir_path: str,
                                        doc_title: str) -> str:
    doc_category = __resolve_doc_category(move_from_dir_path)  # default category: Others
    group = ''
    if not __category_is_group(doc_category, category_group_def):
        group = category_group_def.get_belongs_group(doc_category)
    # change dir name to doc title
    move_to_dir_path = f'{DOCS_DIR_PATH}{group}/{doc_category}/{translate_win_files_unusable_char(doc_title)}/'
    return move_to_dir_path


def __category_is_group(doc_category: str, category_group_def: CategoryGroupDef) -> bool:
    return category_group_def.has_group(doc_category)


def __resolve_target_dir_names(dir_names: List[str]) -> Dict[str, str]:
    # return: key:dir_path value:dir_name
    if len(dir_names) == 0:
        target_dir_names = get_dir_names_in_target_dir(WORK_DIR_PATH)
    else:
        target_dir_names = get_exist_dir_names_in_target_dir(WORK_DIR_PATH, dir_names)
    return {WORK_DIR_PATH + dir_name + '/': dir_name for dir_name in target_dir_names}


def __resolve_doc_category(target_dir_path: str) -> str:
    doc_category = NON_CATEGORY_GROUP_NAME
    category_file_path = target_dir_path + CATEGORY_FILE_NAME
    if os.path.exists(category_file_path):
        doc_categories = read_text_file(category_file_path)
        if len(doc_categories) > 0:
            doc_category = doc_categories[0]
    return doc_category
