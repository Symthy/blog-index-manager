from typing import Optional, Dict, List

from blogs.api.interface import IBlogApiExecutor
from blogs.blog_grouping_deserializer import deserialize_blog_entry_grouping_data
from blogs.hatena.templates.hatena_entry_format import get_blog_summary_index_template, get_blog_entry_template
from common.constant import DOC_IMAGES_DIR_NAME
from docs.doc_set_accessor import get_image_file_paths_in_target_dir
from domain.blog.blog_entry import BlogEntry
from domain.blog.photo_entry import PhotoEntry, PhotoEntries
from domain.doc.doc_entry import DocEntry
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import read_md_file
from files.files_operator import get_updated_time_of_target_file, get_file_name_from_file_path
from files.md_data_handler import join_lines, replace_image_link_in_md_data


def put_hatena_summary_page(api_executor: IBlogApiExecutor, category_group_def: CategoryGroupDef) -> bool:
    """
    ブログのトップページ(summary)を更新する
    :param api_executor:
    :param category_group_def:
    :return:
    """
    entries_grouping_map = deserialize_blog_entry_grouping_data(category_group_def)
    content = get_blog_summary_index_template().format(md_lines=join_lines(entries_grouping_map.convert_md_lines()))
    is_success = api_executor.execute_update_blog_summary_page(content)
    return is_success


def __build_md_file_path(dir_path: str, md_file_name: str):
    return dir_path + md_file_name


# Todo: refactor all

def push_blog_and_photo_entry(api_executor: IBlogApiExecutor, doc_entry: DocEntry, is_draft: bool,
                              old_blog_entry: Optional[BlogEntry] = None) -> Optional[BlogEntry]:
    if old_blog_entry is None:
        # new post
        new_photo_entries_opt = push_photo_entries(api_executor, doc_entry)
        new_blog_entry_opt = push_blog_entry(api_executor, doc_entry, is_draft, new_photo_entries_opt)
        use_photo_entries_opt = new_photo_entries_opt
    else:
        # Overwrite post
        old_photo_entries = None if old_blog_entry.is_images_empty() else old_blog_entry.doc_images
        new_photo_entries_opt: Optional[PhotoEntries] = push_photo_entries(api_executor, doc_entry, old_photo_entries)
        use_photo_entries_opt = old_photo_entries
        if new_photo_entries_opt is not None and not new_photo_entries_opt.is_empty():
            use_photo_entries_opt = new_photo_entries_opt
        new_blog_entry_opt = push_blog_entry(api_executor, doc_entry, is_draft, use_photo_entries_opt,
                                             old_blog_entry.id)
    if new_blog_entry_opt is None:
        return None
    # inherit old image when photo not updated
    new_blog_entry_opt.add_photo_entries(use_photo_entries_opt)
    return new_blog_entry_opt


# public: for testing
def push_blog_entry(api_executor: IBlogApiExecutor, doc_entry: DocEntry, is_draft: bool,
                    photo_entries_opt: Optional[PhotoEntries] = None,
                    old_blog_id_opt: Optional[str] = None) -> Optional[BlogEntry]:
    md_file_path = __build_md_file_path(doc_entry.dir_path, doc_entry.doc_file_name)
    md_file_data = read_md_file(md_file_path)
    if photo_entries_opt is not None:
        md_file_data = replace_image_link_in_md_data(md_file_data, photo_entries_opt)
    title = doc_entry.title
    category = doc_entry.top_category
    content = get_blog_entry_template().format(content=md_file_data)
    # Todo: refactor
    if old_blog_id_opt is None:
        blog_entry_opt = api_executor.execute_register_blog_entry_api(title, category, content, is_draft)
    else:
        blog_entry_opt = api_executor.execute_update_blog_entry_api(old_blog_id_opt, title, category, content, is_draft)
    if blog_entry_opt is None:
        return None
    blog_entry_opt.register_doc_id(doc_entry.id)
    return blog_entry_opt


# public: for testing
def push_photo_entries(api_executor: IBlogApiExecutor, doc_entry: DocEntry,
                       old_photo_entries: Optional[PhotoEntries] = None) -> Optional[PhotoEntries]:
    image_file_paths: List[str] = get_image_file_paths_in_target_dir(f'{doc_entry.dir_path}{DOC_IMAGES_DIR_NAME}')
    if len(image_file_paths) == 0:
        return None
    photo_entry_dict: Dict[str, PhotoEntry] = {}
    for image_file_path in image_file_paths:
        photo_entry_opt = __push_photo_entry(api_executor, image_file_path, old_photo_entries)
        if photo_entry_opt is None:
            continue
        image_filename = get_file_name_from_file_path(image_file_path)
        photo_entry_dict[image_filename] = photo_entry_opt
    return PhotoEntries(photo_entry_dict)


def __push_photo_entry(api_executor: IBlogApiExecutor, image_file_path: str,
                       old_photo_entries: Optional[PhotoEntries] = None) -> Optional[PhotoEntry]:
    image_filename = get_file_name_from_file_path(image_file_path)
    if old_photo_entries is not None and old_photo_entries.is_exist(image_filename):
        image_last_updated = get_updated_time_of_target_file(image_file_path)
        photo_entry = old_photo_entries.get_entry(image_filename)
        if photo_entry.is_after_updated_time(image_last_updated):
            return api_executor.execute_update_photo_entry_api(image_file_path, photo_entry)
        # If don't updated, don't put.
        return
    return api_executor.execute_register_photo_entry_api(image_file_path)
