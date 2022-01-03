import os
import shutil
from typing import List

from common.constant import NON_CATEGORY_NAME, IN_DIR_PATH, DOCS_DIR_PATH
from file.category_group_def import CategoryGroupDef
from file.file_accessor import read_text_file

CATEGORY_FILE_NAME = 'category.txt'


def organize_documents(category_group_def: CategoryGroupDef, dir_names: List[str] = None):
    target_dirs = []
    if dir_names is None:
        files = os.listdir(IN_DIR_PATH)
        target_dirs = [name for name in files if os.path.isdir(os.path.join(IN_DIR_PATH, name))]
    else:
        target_dirs = [d for d in dir_names if
                       os.path.isdir(os.path.join(IN_DIR_PATH, d)) and os.path.exists(os.path.join(IN_DIR_PATH, d))]

    for target_dir in target_dirs:
        move_from_dir_path = IN_DIR_PATH + target_dir + '/'
        doc_category = __resolve_doc_category(move_from_dir_path)  # default: Others
        if category_group_def.is_group(doc_category):
            docs_group_dir_path = DOCS_DIR_PATH + doc_category
            move_to_dir_path = docs_group_dir_path + '/' + target_dir
            shutil.copytree(move_from_dir_path, move_to_dir_path)
        else:
            group = category_group_def.get_belongs_group(doc_category)
            docs_group_category_dir_path = DOCS_DIR_PATH + group + '/' + doc_category
            move_to_dir_path = docs_group_category_dir_path + '/' + target_dir
            shutil.copytree(move_from_dir_path, move_to_dir_path)
        # TODO: original dir delete ?
        shutil.rmtree(move_from_dir_path)


def __resolve_doc_category(target_dir_path: str) -> str:
    doc_category = NON_CATEGORY_NAME
    category_file_path = target_dir_path + CATEGORY_FILE_NAME
    if os.path.exists(category_file_path):
        doc_categories = read_text_file(category_file_path)
        if len(doc_categories) > 0:
            doc_category = doc_categories[0]
    return doc_category
