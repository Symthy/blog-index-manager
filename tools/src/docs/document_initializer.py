import codecs
import os
from typing import Optional, List

from common.constant import IN_DIR_PATH, DOCS_DIR_PATH
from file.category_group_def import CategoryGroupDef
from ltime.time_resolver import resolve_current_time_sequence


def new_local_entry(args: List[str]):
    """
    inディレクトリに新しいdoc枠を生成
    :param args:
    :return:
    """
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
    __create_new_local_entry_set(title, category)


def __create_new_local_entry_set(title: Optional[str], category: Optional[str]):
    if title is None:
        title = 'Entry'  # default value
    if category is None:
        category = ''  # default value
    new_dir_path = IN_DIR_PATH + resolve_current_time_sequence()
    file_name = title + '.md'
    os.mkdir(new_dir_path)
    md_file_path = f'{new_dir_path}/{file_name}'
    with codecs.open(md_file_path, mode='w', encoding='utf-8') as f:
        f.write(f'# {title}\n')
    category_file_path = f'{new_dir_path}/category.txt'
    with codecs.open(category_file_path, mode='w', encoding='utf-8') as f:
        f.write(category)


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
