from typing import Optional, Dict

from blogs.hatena.api_executor import execute_put_hatena_summary_page, execute_post_hatena_blog_register_api, \
    execute_put_hatena_blog_update_api, execute_post_hatena_photo_register_api, execute_put_hatena_photo_update_api
from blogs.hatena.templates.hatena_entry_format import get_blog_summary_index_template, get_blog_entry_template
from common.constant import DOC_IMAGES_DIR_NAME
from domain.blog.blog_entry import BlogEntry
from domain.blog.photo_entry import PhotoEntry, PhotoEntries
from domain.doc.doc_entry import DocEntry
from domain.group_to_categories import GroupToCategorizedEntriesMap
from file.blog_config import BlogConfig
from file.file_accessor import read_md_file
from file.files_operator import get_file_paths_in_target_dir, get_updated_time_of_target_file, get_name_from_path, \
    get_image_file_paths_in_target_dir
from file.md_data_handler import join_lines, replace_image_link_in_md_data


def put_hatena_summary_page(blog_config: BlogConfig, entries_index_map: GroupToCategorizedEntriesMap):
    """
    ブログのトップページ(summary)を更新する
    :param blog_config:
    :param entries_index_map:
    :return:
    """
    content = get_blog_summary_index_template().format(md_lines=join_lines(entries_index_map.convert_md_lines()))
    is_success = execute_put_hatena_summary_page(blog_config, content)
    if not is_success:
        print('[Error] blog summary page update failure')


def __build_md_file_path(dir_path: str, md_file_name: str):
    return dir_path + md_file_name


# Todo: refactor all

def push_blog_and_photo_entry(blog_config, doc_entry: DocEntry, md_file_name: str,
                              old_blog_entry: Optional[BlogEntry] = None) -> Optional[BlogEntry]:
    if old_blog_entry is None:
        __push_photo_entries(blog_config, doc_entry)
        __push_blog_entry(blog_config, doc_entry, md_file_name)
        return None
    old_photo_entries = None if old_blog_entry.is_images_empty() else old_blog_entry.doc_images
    new_photo_entries_opt = __push_photo_entries(blog_config, doc_entry, old_photo_entries)
    new_blog_entry_opt = __push_blog_entry(blog_config, doc_entry, md_file_name, new_photo_entries_opt)
    if new_blog_entry_opt is None:
        return None
    new_blog_entry_opt.add_photo_entries(new_photo_entries_opt)
    return new_blog_entry_opt


def __push_blog_entry(blog_config, doc_entry: DocEntry, md_file_name: str, old_blog_entry_id_opt: Optional[str],
                      updated_photo_entries_opt: Optional[PhotoEntries] = None) -> Optional[BlogEntry]:
    md_file_path = __build_md_file_path(doc_entry.dir_path, md_file_name)
    md_file_data = read_md_file(md_file_path)
    if updated_photo_entries_opt is not None:
        md_file_data = replace_image_link_in_md_data(md_file_data, updated_photo_entries_opt)
    title = doc_entry.title
    category = doc_entry.top_category
    content = get_blog_entry_template().format(content=md_file_data)
    if old_blog_entry_id_opt is None:
        return execute_post_hatena_blog_register_api(blog_config, title, category, content)
    else:
        return execute_put_hatena_blog_update_api(blog_config, old_blog_entry_id_opt, title, category, content)


def __push_photo_entries(blog_config, doc_entry: DocEntry, old_photo_entries: Optional[PhotoEntries] = None) \
        -> Optional[PhotoEntries]:
    image_file_paths = get_image_file_paths_in_target_dir(f'{doc_entry.dir_path}{DOC_IMAGES_DIR_NAME}')
    if len(image_file_paths) == 0:
        return None
    photo_entry_dict: Dict[str, PhotoEntry] = {}
    for image_file_path in image_file_paths:
        photo_entry_opt = __push_photo_entry(blog_config, image_file_path, old_photo_entries)
        if photo_entry_opt is None:
            continue
        image_filename = get_name_from_path(image_file_path)
        photo_entry_dict[image_filename] = photo_entry_opt
    return PhotoEntries(photo_entry_dict)


def __push_photo_entry(blog_config, image_file_path: str, old_photo_entries: Optional[PhotoEntries] = None) \
        -> Optional[PhotoEntry]:
    if old_photo_entries is not None and old_photo_entries.is_exist(image_file_path):
        image_filename = get_name_from_path(image_file_path)
        image_last_updated = get_updated_time_of_target_file(image_file_path)
        if old_photo_entries.get_entry(image_filename).is_after_updated_time(image_last_updated):
            return execute_put_hatena_photo_update_api(blog_config, image_file_path)
        # If don't updated, don't put.
        return
    return execute_post_hatena_photo_register_api(blog_config, image_file_path)
