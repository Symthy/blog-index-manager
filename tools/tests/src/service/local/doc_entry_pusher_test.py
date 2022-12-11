import os
import shutil

import pytest
from mock import mock

import service.local.doc_entry_pusher as pusher
from docs.docs_backuper import DocsBackuper
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from docs.docs_mover import DocsMover
from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.doc.doc_entry import DocEntry, DocEntries
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from files.conf.category_group_def import CategoryGroupDef
from service.entry_summary_factory import EntrySummaryFactory
from service.local.doc_entry_summary_writer import DocEntrySummaryWriter
from tools.tests.fixture.path_builder import build_test_data_path, test_root_dir_path

PUSHER_TEST_DATA_DIR_PATH = 'service/local/pusher/'


@pytest.fixture(scope='module', autouse=True)
def before_and_after_all():
    current_dir = os.curdir
    os.chdir(test_root_dir_path())
    yield
    os.chdir(current_dir)
    bk_data_dir_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'bk/data/')
    data_dir_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'data/')
    local_entry_data_dir_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'data/local_entry_data/')
    shutil.rmtree(local_entry_data_dir_path)
    shutil.copytree(bk_data_dir_path, data_dir_path, dirs_exist_ok=True)
    bk_work_dir_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'bk/work/')
    work_dir_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'work/')
    shutil.rmtree(work_dir_path)
    os.mkdir(work_dir_path)
    shutil.copytree(bk_work_dir_path, work_dir_path, dirs_exist_ok=True)


def build_doc_entry_pusher():
    dump_dir_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'data/local_entry_data/')
    docs_entry_accessor = DumpEntryAccessor(dump_dir_path, DocEntry.restore_from_json_data)

    entry_list_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'data/local_entry_list.json')
    docs_entries_accessor = DumpEntriesAccessor(entry_list_path, docs_entry_accessor, DocEntries.new_instance)

    yml_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'data/category_group_def.yml')
    category_group_def = CategoryGroupDef.load_category_group_def_yaml(yml_path)
    grouping_file_path = build_test_data_path(PUSHER_TEST_DATA_DIR_PATH + 'data/local_entry_grouping.json')

    docs_grouping_data_deserializer = DocsGroupingDataDeserializer(docs_entries_accessor, category_group_def,
                                                                   grouping_file_path)

    mock_blog_entries_accessor: DumpEntriesAccessor[BlogEntries, BlogEntry] = mock.MagicMock()
    entry_summary_factory = EntrySummaryFactory(docs_entries_accessor, mock_blog_entries_accessor, category_group_def,
                                                docs_grouping_data_deserializer)
    entry_summary_writer = DocEntrySummaryWriter(entry_summary_factory)

    mock_docs_backuper: DocsBackuper = mock.MagicMock()

    work_dir_path = './test_data/service/local/pusher/work/'
    docs_mover = DocsMover(category_group_def, work_dir_path)
    return pusher.DocEntryPusher(docs_entries_accessor, category_group_def, entry_summary_writer, mock_docs_backuper,
                                 docs_mover, docs_grouping_data_deserializer)


def test_push_documents_to_docs(mocker):
    move_dir_mock = mocker.patch('service.local.doc_entry_pusher.move_documents_to_docs_dir', return_value=None)
    doc_entry_pusher = build_doc_entry_pusher()

    add_doc_dir_names = ['test_doc_10', 'test_doc_11', 'test_doc_12']
    entries = doc_entry_pusher.execute(False, add_doc_dir_names)

    move_dir_mock.assert_called_once()
    assert entries.size() == 3
    for entry in entries.entry_list:
        if entry.dir_path.endswith('test_doc_10/'):
            assert entry.pickup is False
            assert entry.title == 'test doc 10'
            assert entry.dir_path == './docs/Program/Golang/test_doc_10/'
            assert entry.top_category == 'Golang'
            assert entry.categories == ['Golang']
            assert entry.doc_file_name == 'doc.md'
        elif entry.dir_path.endswith('test_doc_11/'):
            assert entry.pickup is False
            assert entry.title == 'test doc 11'
            assert entry.dir_path == './docs/FrontEnd/test_doc_11/'
            assert entry.top_category == 'FrontEnd'
            assert entry.categories == ['FrontEnd']
            assert entry.doc_file_name == 'doc.md'
        elif entry.dir_path.endswith('test_doc_12/'):
            assert entry.pickup is False
            assert entry.title == 'test doc 12'
            assert entry.dir_path == './docs/Others/test_doc_12/'
            assert entry.top_category == 'Others'
            assert entry.categories == []
            assert entry.doc_file_name == 'doc.md'
        else:
            assert False
        assert os.path.exists(
            f'./test_data/service/local/pusher/data/local_entry_data/{entry.id}.json'.replace('/', os.sep))
    # Todo: validate in file
