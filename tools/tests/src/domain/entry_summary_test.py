from domain.category_to_entries import CategoryToEntriesMap
from domain.doc.doc_entry import DocEntry, DocEntries
from domain.entry_summary import EntrySummary
from domain.group_to_categories import GroupToCategorizedEntriesMap
from files.conf.category_group_def import CategoryGroupDef


def test_entry_summary():
    entry1 = DocEntry('20221201010000', "title 1", "dummy dir path 1/", "doc.md", ["Group1"], False)
    entry2 = DocEntry('20221201020000', "title 2", "dummy dir path 2/", "doc.md", ["Category1"], False)
    entry3 = DocEntry('20221201030000', "title 3", "dummy dir path 3/", "doc.md", ["Category2"], False)
    entry4 = DocEntry('20221201040000', "title 4", "dummy dir path 4/", "doc.md", ["Group2"], False)
    entry5 = DocEntry('20221201050000', "title 5", "dummy dir path 5/", "doc.md", ["Category3"], True)
    entry6 = DocEntry('20221201060000', "title 6", "dummy dir path 6/", "doc.md", ["Category1"], True)
    group_to_categories_json = [
        {'Group1': ["Category1", "Category2"]},
        {'Group2': ["Category3"]}
    ]

    category_group_def = CategoryGroupDef(group_to_categories_json)
    category_group_def.print_data()
    category_entries = CategoryToEntriesMap(DocEntries([entry1, entry2, entry3, entry4, entry5, entry6]))
    grouping_entries = GroupToCategorizedEntriesMap(category_group_def, category_entries)

    actual_lines = EntrySummary(DocEntries([entry5, entry6]), grouping_entries).pickup_and_all_entry_lines
    print(actual_lines)
    expect_lines = [
        "Pickup:",
        "- [title 5](dummy dir path 5/doc.md)",
        "- [title 6](dummy dir path 6/doc.md)",
        "",
        "All:",
        "- Group1",
        "  - Category1",
        "    - [title 2](dummy dir path 2/doc.md)",
        "    - [title 6](dummy dir path 6/doc.md)",
        "  - Category2",
        "    - [title 3](dummy dir path 3/doc.md)",
        "  - [title 1](dummy dir path 1/doc.md)",
        "- Group2",
        "  - Category3",
        "    - [title 5](dummy dir path 5/doc.md)",
        "  - [title 4](dummy dir path 4/doc.md)",
        "- Others"
    ]
    assert expect_lines == actual_lines
