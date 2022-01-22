from typing import Dict

from common.constant import LOCAL_DOCS_ENTRY_LIST_PATH
from files.file_accessor import load_json


# Todo: refactor
def load_docs_entries_json() -> Dict[str, str]:
    local_entry_list_json = load_json(LOCAL_DOCS_ENTRY_LIST_PATH)
    if not 'entries' in local_entry_list_json:
        return {}
    return local_entry_list_json['entries']


def is_exist_in_local_entry_list(entry_id: str) -> bool:
    local_entry_list_json = load_json(LOCAL_DOCS_ENTRY_LIST_PATH)
    if not 'entries' in local_entry_list_json:
        return False
    entry_id_to_title = local_entry_list_json['entries']
    return entry_id in entry_id_to_title


def get_local_doc_entry_dump_data(entry_id: str) -> Dict[str, str]:
    entry_dump_file_path = f'{LOCAL_DOCS_ENTRY_DUMP_DIR}{entry_id}.json'
    entry_dump_data = load_json(entry_dump_file_path)
    return entry_dump_data
