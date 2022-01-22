from typing import Optional, List

from common.constant import DOC_TITLE_MAX_LENGTH, DOC_IMAGES_DIR_NAME, WORK_DIR_PATH, CATEGORY_FILE_NAME
from files.files_operator import make_new_file, make_new_dir, translate_win_files_unusable_char
from ltime.time_resolver import resolve_current_time_date_time


def new_local_document_set(cmd_args: List[str]) -> Optional[str]:
    """
    inディレクトリに新しいdocセットを生成
    :param cmd_args:
    :return:
    """

    def resolve_option(args: List[str]):
        title = None
        category = None
        t_index = -1
        c_index = -1
        # Todo: refactor
        if '-t' in args:
            t_index = args.index('-t')
        if '-title' in args:
            t_index = args.index('-title')
        if t_index != -1 and len(args) > t_index + 1 and not args[t_index + 1].startswith('-'):
            title = args[t_index + 1]
        if '-c' in args:
            c_index = args.index('-c')
        if '-category' in args:
            c_index = args.index('-category')
        if c_index != -1 and len(args) > c_index + 1 and not args[c_index + 1].startswith('-'):
            category = args[c_index + 1]
        return title, category

    title_value_opt, category_value_opt = resolve_option(cmd_args)
    if title_value_opt is not None:
        if len(title_value_opt) > DOC_TITLE_MAX_LENGTH or len(title_value_opt) == 0:
            print(f'[ERROR] title is too long ({DOC_TITLE_MAX_LENGTH} characters or less)')
            return None
    return __create_local_document_set(title_value_opt, category_value_opt)


def __create_local_document_set(title: Optional[str], category: Optional[str]) -> str:
    if title is None:
        title = 'doc'  # default value
    if category is None:
        category = ''  # default value
    dir_name = resolve_current_time_date_time()
    new_dir_path = f'{WORK_DIR_PATH}{dir_name}'
    make_new_dir(new_dir_path)
    md_file_path = f'{new_dir_path}/{translate_win_files_unusable_char(title)}.md'
    make_new_file(md_file_path, f'# {title}\n')
    category_file_path = f'{new_dir_path}/{CATEGORY_FILE_NAME}'
    make_new_file(category_file_path, category)
    make_new_dir(f'{new_dir_path}/{DOC_IMAGES_DIR_NAME}')
    return dir_name
