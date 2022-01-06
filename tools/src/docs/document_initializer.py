import os
from typing import Optional, List

from common.constant import WORK_DIR_PATH, DOCS_DIR_PATH, DOC_TITLE_MAX_LENGTH
from file.category_group_def import CategoryGroupDef
from file.files_operator import make_new_file, make_new_dir, translate_win_files_unusable_char
from ltime.time_resolver import resolve_current_time_sequence


def new_local_document_set(cmd_args: List[str]) -> str:
    """
    inディレクトリに新しいdocセットを生成
    :param cmd_args:
    :return:
    """

    def resolve_option(args: List[str]):
        title = None
        category = None
        if '-t' in args:
            t_index = args.index('-t')
            if t_index != -1 and len(args) > t_index + 1:
                title = args[t_index + 1]
                args = args[t_index + 1:]
        if '-c' in args:
            c_index = args.index('-c')
            if c_index != -1 and len(args) > c_index + 1:
                category = args[c_index + 1]
        return title, category

    title_value, category_value = resolve_option(cmd_args)
    if title_value is None:
        title_value = resolve_current_time_sequence()
    if len(title_value) > DOC_TITLE_MAX_LENGTH or len(title_value) <= 0:
        raise Exception(f'[ERROR] title is too long ({DOC_TITLE_MAX_LENGTH} characters or less)')
    __create_local_document_set(title_value, category_value)
    return title_value


def __create_local_document_set(title: Optional[str], category: Optional[str]):
    if title is None:
        title = 'doc'  # default value
    if category is None:
        category = ''  # default value
    current_time_sequence = resolve_current_time_sequence()
    new_dir_path = WORK_DIR_PATH + current_time_sequence
    make_new_dir(new_dir_path)
    md_file_path = f'{new_dir_path}/{translate_win_files_unusable_char(title)}.md'
    make_new_file(md_file_path, f'# {title}\n')
    category_file_path = f'{new_dir_path}/category.txt'
    make_new_file(category_file_path, category)
    created_time_file = f'{new_dir_path}/{current_time_sequence}'
    make_new_file(created_time_file)


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
