import os

import pytest

from common.constant import DOCS_DIR_PATH_TEMP_FILE
from docs.docs_backuper import DocsBackuper
from docs.docs_grouping_data_deserializer import DocsGroupingDataDeserializer
from domain.doc.doc_entry import DocEntry, DocEntries
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.file_accessor import read_file_first_line
from files.files_operator import is_exist_dir, is_exist_file
from service.local.doc_entry_retriever import DocEntryRetriever
from tools.tests.fixture.path_builder import build_test_data_path, test_root_dir_path

BACKUP_DIR_PATH_FOR_TESTING = build_test_data_path('service/local/retriever/backup/')
WORK_DIR_PATH_FOR_TESTING = build_test_data_path('service/local/retriever/work/')
DOCS_DIR_PATH_FOR_TESTING = build_test_data_path('service/local/retriever/docs')
RETRIEVER_TEST_DATA_DIR_PATH = 'service/local/retriever/data/'


@pytest.fixture(scope='module', autouse=True)
def before_and_after_all():
    current_dir = os.curdir
    os.chdir(test_root_dir_path())
    if not os.path.exists(BACKUP_DIR_PATH_FOR_TESTING):
        os.mkdir(BACKUP_DIR_PATH_FOR_TESTING)
    if not os.path.exists(WORK_DIR_PATH_FOR_TESTING):
        os.mkdir(WORK_DIR_PATH_FOR_TESTING)
    yield
    os.chdir(current_dir)


@pytest.fixture
def doc_entry_retriever() -> DocEntryRetriever:
    dump_dir_path = build_test_data_path(RETRIEVER_TEST_DATA_DIR_PATH + 'local_entry_data/')
    docs_entry_accessor = DumpEntryAccessor(dump_dir_path, DocEntry.restore_from_json_data)
    entry_list_path = build_test_data_path(RETRIEVER_TEST_DATA_DIR_PATH + 'local_entry_list.json')
    docs_entries_accessor = DumpEntriesAccessor(entry_list_path, docs_entry_accessor, DocEntries.new_instance)
    docs_backuper = DocsBackuper(BACKUP_DIR_PATH_FOR_TESTING, WORK_DIR_PATH_FOR_TESTING)
    yml_path = build_test_data_path(RETRIEVER_TEST_DATA_DIR_PATH + 'category_group_def.yml')
    category_group_def = CategoryGroupDef.load_category_group_def_yaml(yml_path)
    grouping_file_path = build_test_data_path(RETRIEVER_TEST_DATA_DIR_PATH + 'local_entry_grouping.json')

    deserializer = DocsGroupingDataDeserializer(docs_entries_accessor, category_group_def, grouping_file_path)
    return DocEntryRetriever(docs_entries_accessor, docs_backuper, deserializer)


def test_retrieve_and_cancel(doc_entry_retriever):
    entry_id = '20221201000000'

    doc_entry_retriever.retrieve_document_from_docs([entry_id])
    assert is_exist_dir(os.path.join(BACKUP_DIR_PATH_FOR_TESTING, entry_id))
    assert is_exist_file(os.path.join(BACKUP_DIR_PATH_FOR_TESTING, entry_id, 'doc.md'))
    master_path_temp_path = os.path.join(BACKUP_DIR_PATH_FOR_TESTING, entry_id, DOCS_DIR_PATH_TEMP_FILE)
    assert is_exist_file(master_path_temp_path)
    assert read_file_first_line(
        master_path_temp_path) == './test_data/service/local/retriever/docs/Program/Golang/test_doc_1'
    assert is_exist_dir(os.path.join(WORK_DIR_PATH_FOR_TESTING, 'test_doc_1'))
    assert is_exist_file(os.path.join(WORK_DIR_PATH_FOR_TESTING, 'test_doc_1', 'doc.md'))
    assert not is_exist_dir(os.path.join(DOCS_DIR_PATH_FOR_TESTING, 'Program', 'Golang', 'test_doc_1'))

    doc_entry_retriever.cancel_retrieving_document([entry_id])
    assert not is_exist_dir(os.path.join(BACKUP_DIR_PATH_FOR_TESTING, entry_id))
    assert not is_exist_file(os.path.join(BACKUP_DIR_PATH_FOR_TESTING, entry_id, 'doc.md'))
    assert not is_exist_dir(os.path.join(WORK_DIR_PATH_FOR_TESTING, 'test_doc_1'))
    assert not is_exist_file(os.path.join(WORK_DIR_PATH_FOR_TESTING, 'test_doc_1', 'doc.md'))
    assert is_exist_dir(os.path.join(DOCS_DIR_PATH_FOR_TESTING, 'Program', 'Golang', 'test_doc_1'))
    assert not is_exist_file(
        os.path.join(DOCS_DIR_PATH_FOR_TESTING, 'Program', 'Golang', 'test_doc_1', DOCS_DIR_PATH_TEMP_FILE))
