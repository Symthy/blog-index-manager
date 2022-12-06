import pytest

from domain.doc.doc_entry import DocEntry, DocEntries
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from ltime.time_resolver import convert_entry_time_str_to_datetime
from tools.tests.fixture.path_builder import build_test_data_path


@pytest.fixture
def docs_entries_accessor():
    dump_dir_path = build_test_data_path('dump/data/local_entry_data/')
    docs_entry_accessor = DumpEntryAccessor(dump_dir_path, DocEntry.restore_from_json_data)
    entry_list_path = build_test_data_path('dump/data/local_entry_list.json')
    return DumpEntriesAccessor(entry_list_path, docs_entry_accessor, DocEntries.new_instance)


def test_load_entry(docs_entries_accessor: DumpEntriesAccessor):
    expect: DocEntries = DocEntries.new_instance([
        DocEntry("20221201000000", "test document 0", "./test/docs/md_data", "doc.md", [], False,
                 convert_entry_time_str_to_datetime("2022-12-01T00:00:00"),
                 None),
        DocEntry("20221201010000", "test document 1", "./test/docs/md_data", "doc.md", [], False,
                 convert_entry_time_str_to_datetime("2022-12-01T01:00:00"),
                 convert_entry_time_str_to_datetime("2022-12-01T01:00:01")),
        DocEntry("20221201020000", "test document 2", "./test/docs/md_data", "doc.md", [], True,
                 convert_entry_time_str_to_datetime("2022-12-01T02:00:00"),
                 convert_entry_time_str_to_datetime("2022-12-01T02:00:02"))
    ])
    actual: DocEntries = docs_entries_accessor.load_entries()
    assert expect == actual
