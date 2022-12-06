import os

import pytest

from docs.docs_backuper import DocsBackuper
from domain.doc.doc_entry import DocEntry, DocEntries
from dump.dump_entries_accessor import DumpEntriesAccessor
from dump.dump_entry_accessor import DumpEntryAccessor
from files.conf.category_group_def import CategoryGroupDef
from files.files_operator import is_exist_dir, is_exist_file
from service.local.doc_entry_retriever import DocEntryRetriever
from tools.tests.fixture.path_builder import build_test_data_path

BACKUP_DIR_PATH_FOR_TESTING = build_test_data_path('service/local/retriever/backup/')


@pytest.fixture
def docs_entries_accessor():
    dump_dir_path = build_test_data_path('service/local/retriever/data/local_entry_data/')
    docs_entry_accessor = DumpEntryAccessor(dump_dir_path, DocEntry.restore_from_json_data)
    entry_list_path = build_test_data_path('service/local/retriever/data/local_entry_list.json')
    return DumpEntriesAccessor(entry_list_path, docs_entry_accessor, DocEntries.new_instance)


@pytest.fixture
def docs_backuper():
    return DocsBackuper(BACKUP_DIR_PATH_FOR_TESTING)


@pytest.fixture
def category_group_def():
    yml_path = build_test_data_path('service/local/retriever/data/category_group_def.yml')
    category_group_def = CategoryGroupDef.load_category_group_def_yaml(yml_path)
    return category_group_def


def test_retrieve_and_cancel(docs_entries_accessor, docs_backuper, category_group_def):
    retriever = DocEntryRetriever(docs_entries_accessor, docs_backuper, category_group_def)
    retriever.retrieve_document_from_docs(["20221201000000"])
    assert is_exist_dir(os.path.join(BACKUP_DIR_PATH_FOR_TESTING, 'test_doc_1')) is True
    assert is_exist_file(os.path.join(BACKUP_DIR_PATH_FOR_TESTING, 'test_doc_1/doc.md')) is True
