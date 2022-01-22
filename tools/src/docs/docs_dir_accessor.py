from typing import Optional, Dict

from common.constant import LOCAL_DOCS_ENTRY_DUMP_DIR
from files.file_accessor import read_file_first_line, load_json


def get_doc_title_from_md_file(doc_md_file_path: str) -> Optional[str]:
    doc_title = read_file_first_line(doc_md_file_path)
    if len(doc_title) == 0:
        return None
    return doc_title



