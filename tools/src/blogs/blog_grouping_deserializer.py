from blogs.dump_blog_entries_accessor import DumpBlogEntriesAccessor
from domain.category_to_entries import CategoryToEntriesMap
from domain.group_to_categories import GroupToCategorizedEntriesMap
from files.conf.category_group_def import CategoryGroupDef


def deserialize_blog_entry_grouping_data(category_group_def: CategoryGroupDef) -> GroupToCategorizedEntriesMap:
    blog_entries = DumpBlogEntriesAccessor().load_entries()
    category_to_entries = CategoryToEntriesMap(blog_entries)
    blog_entry_grouping_map = GroupToCategorizedEntriesMap(category_group_def, category_to_entries)
    return blog_entry_grouping_map
