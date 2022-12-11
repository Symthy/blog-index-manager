import shutil

import pytest
from mock import mock

from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.doc.doc_entry import DocEntry, DocEntries
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from files.conf.category_group_def import CategoryGroupDef
from service.entry_summary_factory import EntrySummaryFactory
from service.local.doc_entry_summary_writer import DocEntrySummaryWriter
from service.local.doc_entry_updater import DocEntryUpdater
from tools.tests.fixture.path_builder import build_test_data_path

UPDATER_TEST_DATA_DIR_PATH = 'service/local/updater/'


@pytest.fixture(scope='module', autouse=True)
def before_and_after_all():
    yield
    bk_data_dir_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'bk/local_entry_data/')
    data_dir_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'data/local_entry_data/')
    shutil.rmtree(data_dir_path)
    shutil.copytree(bk_data_dir_path, data_dir_path, dirs_exist_ok=True)


@pytest.fixture
def doc_entry_updater():
    yml_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'data/category_group_def.yml')
    category_group_def = CategoryGroupDef.load_category_group_def_yaml(yml_path)
    grouping_file_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'data/local_entry_grouping.json')

    dump_dir_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'data/local_entry_data/')
    docs_entry_accessor = DumpEntryAccessor(dump_dir_path, DocEntry.restore_from_json_data)
    entry_list_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'data/local_entry_list.json')
    docs_entries_accessor = DumpEntriesAccessor(entry_list_path, docs_entry_accessor, DocEntries.new_instance)
    docs_grouping_data_deserializer = DocsGroupingDataDeserializer(docs_entries_accessor, category_group_def,
                                                                   grouping_file_path)

    mock_blog_entries_accessor: DumpEntriesAccessor[BlogEntries, BlogEntry] = mock.MagicMock()
    entry_summary_factory = EntrySummaryFactory(docs_entries_accessor, mock_blog_entries_accessor, category_group_def,
                                                docs_grouping_data_deserializer)
    entry_summary_writer = DocEntrySummaryWriter(entry_summary_factory)
    return DocEntryUpdater(docs_entries_accessor, entry_summary_writer)


def test_update_pickup(doc_entry_updater):
    dump_dir_path = build_test_data_path(UPDATER_TEST_DATA_DIR_PATH + 'data/local_entry_data/')
    docs_entry_accessor = DumpEntryAccessor(dump_dir_path, DocEntry.restore_from_json_data)
    entry_before = docs_entry_accessor.load_entry('20221201000000')
    assert entry_before.pickup is False
    doc_entry_updater.update_pickup('20221201000000', True)
    entry_after = docs_entry_accessor.load_entry('20221201000000')
    assert entry_after.pickup is True
