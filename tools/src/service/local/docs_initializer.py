from common.constant import DOCS_DIR_PATH
from files.conf.category_group_def import CategoryGroupDef
from files.files_operator import get_files, make_new_dir, is_exist_dir, delete_dir


def initialize_docs_dir(category_group_def: CategoryGroupDef):
    """
    docsディレクトリ配下をCategoryGroup定義に基づきディレクトリ作成
    :param category_group_def:
    :return:
    """
    if not is_exist_dir(DOCS_DIR_PATH):
        make_new_dir(DOCS_DIR_PATH)
    for group in category_group_def.groups:
        docs_group_dir_path = DOCS_DIR_PATH + group + '/'
        if not is_exist_dir(docs_group_dir_path):
            make_new_dir(docs_group_dir_path)
        for category in category_group_def.get_categories(group):
            docs_group_category_dir_path = docs_group_dir_path + category + '/'
            if not is_exist_dir(docs_group_category_dir_path):
                continue
            # remove empty category dir
            if len(get_files(docs_group_category_dir_path)) == 0:
                delete_dir(docs_group_category_dir_path)
