import os

from common.constant import DOCS_DIR_PATH
from files.category_group_def import CategoryGroupDef


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
