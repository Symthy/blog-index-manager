from common.constant import HATENA_BLOG_ENTRY_INDEX_RESULT_PATH
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.category_to_entries import CategoryToEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import write_text_lines


def update_blog_entry_summary_file(dump_blog_data_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
                                   category_group_def: CategoryGroupDef,
                                   updated_blog_entries: BlogEntries) -> GroupToCategorizedEntriesMap:
    blog_entries: BlogEntries = dump_blog_data_accessor.load_entries()
    blog_entries.merge(updated_blog_entries)
    category_to_entries = CategoryToEntriesMap(blog_entries)
    # print_md_lines(category_to_entries)
    entries_index_map = GroupToCategorizedEntriesMap(category_group_def, category_to_entries)
    # print_md_lines(entries_index_map)
    write_text_lines(HATENA_BLOG_ENTRY_INDEX_RESULT_PATH, entries_index_map.convert_md_lines())
    return entries_index_map
