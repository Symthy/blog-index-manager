import os
from typing import List, Optional, Dict

from common.constant import NON_CATEGORY_GROUP_NAME, WORK_DIR_PATH, DOCS_DIR_PATH, CATEGORY_FILE_NAME
from docs.doc_set_accessor import get_md_file_path_in_target_dir, get_doc_title_from_md_file
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import read_text_file
from files.files_operator import get_dir_names_in_target_dir, get_exist_dir_names_in_target_dir, \
    translate_win_files_unusable_char, move_dir


def move_documents_to_docs_dir(moving_from_to_path_dict: Dict[str, str]):
    for from_dir_path, to_dir_path in moving_from_to_path_dict.items():
        move_dir(from_dir_path, to_dir_path)


class DocsMover:
    def __init__(self, category_group_def: CategoryGroupDef, work_dir_path: str = WORK_DIR_PATH):
        self.__category_group_def = category_group_def
        self.__work_dir_path = work_dir_path

    def resolve_moving_from_and_to_dir_path(self, target_dir_names: List[str]) \
            -> Dict[str, str]:
        # return: key:move_from_path value: move_to_path
        target_dir_path_to_name_dict = self.__resolve_target_dir_names(target_dir_names)
        path_dict = {}
        for move_from_dir_path in target_dir_path_to_name_dict:
            md_file_path: Optional[str] = get_md_file_path_in_target_dir(move_from_dir_path)
            if md_file_path is None:
                # skip when non exist md file in target dir
                print(
                    f'[Info] skip move dir: non exist md file (dir: {target_dir_path_to_name_dict[move_from_dir_path]})')
                continue
            doc_title: Optional[str] = get_doc_title_from_md_file(md_file_path)
            if doc_title is None:
                print(f'[Warn] empty doc title (dir: {target_dir_path_to_name_dict[move_from_dir_path]})')
                continue
            move_to_dir_path = self.__resolve_move_to_dir_path(move_from_dir_path, doc_title)
            path_dict[move_from_dir_path] = move_to_dir_path
        return path_dict

    def __resolve_move_to_dir_path(self, move_from_dir_path: str,
                                   doc_title: str) -> str:
        def __resolve_doc_category(target_dir_path: str) -> str:
            category = NON_CATEGORY_GROUP_NAME
            category_file_path = target_dir_path + CATEGORY_FILE_NAME
            if os.path.exists(category_file_path):
                doc_categories = read_text_file(category_file_path)
                if len(doc_categories) > 0:
                    category = doc_categories[0]
            return category

        doc_category = __resolve_doc_category(move_from_dir_path)  # default category: Others
        group_dir = ''
        if not self.__category_is_group(doc_category):
            group_dir = f'{self.__category_group_def.get_belongs_group(doc_category)}/'
        group_and_category_part_path = f'{group_dir}{doc_category}'
        # change dir name to doc title
        move_to_dir_path = f'{DOCS_DIR_PATH}{group_and_category_part_path}/{translate_win_files_unusable_char(doc_title)}/'
        return move_to_dir_path

    def __category_is_group(self, doc_category: str) -> bool:
        return self.__category_group_def.has_group(doc_category)

    def __resolve_target_dir_names(self, dir_names: List[str]) -> Dict[str, str]:
        # return: key:dir_path value:dir_name
        if len(dir_names) == 0:
            target_dir_names = get_dir_names_in_target_dir(self.__work_dir_path)
        else:
            target_dir_names = get_exist_dir_names_in_target_dir(self.__work_dir_path, dir_names)
        return {self.__work_dir_path + dir_name + '/': dir_name for dir_name in target_dir_names}
