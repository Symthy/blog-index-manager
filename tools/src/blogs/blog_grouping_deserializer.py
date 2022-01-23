from blogs.dump_blog_entries_accessor import DumpBlogEntriesAccessor
from domain.group_to_categories import GroupToCategorizedEntriesMap
from files.conf.category_group_def import CategoryGroupDef


def deserialize_blog_entry_grouping_data(category_group_def: CategoryGroupDef) -> GroupToCategorizedEntriesMap:
    entry_grouping_map = GroupToCategorizedEntriesMap.deserialize_entry_grouping_data(DumpBlogEntriesAccessor(),
                                                                                      category_group_def)
    return entry_grouping_map
