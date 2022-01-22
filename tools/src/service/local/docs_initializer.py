import os
from typing import Optional, List

from common.constant import WORK_DIR_PATH, DOCS_DIR_PATH, DOC_TITLE_MAX_LENGTH, CATEGORY_FILE_NAME, DOC_IMAGES_DIR_NAME
from file.category_group_def import CategoryGroupDef
from file.files_operator import make_new_file, make_new_dir, translate_win_files_unusable_char
from ltime.time_resolver import resolve_current_time_date_time


def initialize_docs_dir(category_group_def: CategoryGroupDef):
    """
    docsディレクトリ配下をCategoryGroup定義に基づきディレクトリ作成
    :param category_group_def:
    :return:
    """
    if not os.path.exists(DOCS_DIR_PATH):
        os.mkdir(DOCS_DIR_PATH)
    for group in category_group_def.groups:
        docs_group_dir_path = DOCS_DIR_PATH + group + '/'
        if not os.path.exists(docs_group_dir_path):
            os.mkdir(docs_group_dir_path)
        for category in category_group_def.get_categories(group):
            docs_group_category_dir_path = docs_group_dir_path + category + '/'
            if os.path.exists(docs_group_category_dir_path):
                # remove empty category dir
                if len(os.listdir(docs_group_category_dir_path)) > 0:
                    os.remove(docs_group_category_dir_path)
