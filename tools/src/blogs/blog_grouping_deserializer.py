from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.category_to_entries import CategoryToEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from dump.interface import IDumpEntriesAccessor
from files.conf.category_group_def import CategoryGroupDef


def deserialize_grouping_blog_entries(
        blog_entries_accessor: IDumpEntriesAccessor[BlogEntries, BlogEntry],
        category_group_def: CategoryGroupDef) -> GroupToCategorizedEntriesMap:
    blog_entries = blog_entries_accessor.load_entries()
    # print(join_lines(blog_entries.convert_md_lines()))
    category_to_entries = CategoryToEntriesMap(blog_entries)
    # print(join_lines(category_to_entries.convert_md_lines()))
    grouping_blog_entries_map = GroupToCategorizedEntriesMap(category_group_def, category_to_entries)
    # print(join_lines(grouping_blog_entries_map.convert_md_lines()))
    return grouping_blog_entries_map
