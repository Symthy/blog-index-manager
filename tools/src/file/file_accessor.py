import base64
import codecs
import configparser
import json
from typing import List, Dict, Optional

import yaml

from common.constant import CATEGORY_GROUP_YAML_PATH, LOCAL_DOCS_ENTRY_LIST_PATH, LOCAL_DOCS_ENTRY_DUMP_DIR
from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef
from file.md_data_handler import join_lines


def read_blog_config(config_path):
    conf_parser = configparser.ConfigParser()
    conf_parser.read(config_path)
    return BlogConfig(conf_parser)


def read_file_first_line(file_path: str):
    with codecs.open(file_path, mode='r', encoding='utf-8') as f:
        line = f.readline()
    return line.lstrip('#').strip()


def read_text_file(file_path: str) -> List[str]:
    try:
        with codecs.open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            lines_exclusion_empty = list(filter(lambda line: line.replace(' ', '').replace('\n', '') != '', lines))
            lines_exclusion_comment = list(filter(lambda line: not line.startswith('#'), lines_exclusion_empty))
            return [line.replace('\n', '') for line in lines_exclusion_comment]
    except Exception as e:
        print(f'[Warning] Invalid {file_path}, read failure:', e)
        return []


def read_md_file(file_path: str) -> str:
    with codecs.open(file_path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    return join_lines(lines)


def read_pic_file_b64(pic_file_path: str) -> str:
    with open(pic_file_path, 'rb') as f:
        pic_data = f.read()
    return base64.b64encode(pic_data).decode('utf-8')


def __write_text_file(file_path, text: str):
    try:
        with codecs.open(file_path, mode='w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(f'[Warning] Invalid {file_path}, write failure:', e)


def write_text_line(file_path, line: str):
    __write_text_file(file_path, line)


def write_text_lines(file_path, lines: List[str]):
    __write_text_file(file_path, '\n'.join(lines))


def load_json(file_path):
    with codecs.open(file_path, mode='r', encoding='utf-8') as file:
        obj = json.load(file)
    return obj


def dump_json(file_path, dump_data):
    with codecs.open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(dump_data, file, indent=2, ensure_ascii=False)


def load_category_group_def_yaml() -> CategoryGroupDef:
    json_data = load_yaml(CATEGORY_GROUP_YAML_PATH)  # return list
    return CategoryGroupDef(json_data)


def load_yaml(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        obj = yaml.safe_load(file)
    return obj


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


def get_doc_title_from_md_file(doc_md_file_path: str) -> Optional[str]:
    doc_title = read_file_first_line(doc_md_file_path)
    if len(doc_title) == 0:
        return None
    return doc_title


def get_local_doc_entry_dump_data(entry_id: str) -> Dict[str, str]:
    entry_dump_file_path = f'{LOCAL_DOCS_ENTRY_DUMP_DIR}{entry_id}'
    entry_dump_data = load_json(entry_dump_file_path)
    return entry_dump_data


def get_dir_path_from_local_entry_dump_data(entry_id: str) -> str:
    entry_dump_data = get_local_doc_entry_dump_data(entry_id)
    target_entry_dir_path = entry_dump_data['dir_path']
    return target_entry_dir_path
