import base64
import codecs
import configparser
import json
from typing import List

import yaml

from files.conf.blog_config import BlogConfig
from files.files_operator import is_exist_file


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
            lines_exclusion_empty = list(
                filter(lambda line: line.replace(' ', '').replace('\r', '').replace('\n', '') != '', lines))
            lines_exclusion_comment = list(filter(lambda line: not line.startswith('#'), lines_exclusion_empty))
            return [line.replace('\r', '').replace('\n', '') for line in lines_exclusion_comment]
    except Exception as e:
        print(f'[Warning] Invalid {file_path}, read failure:', e)
        return []


def read_md_file(file_path: str) -> str:
    with codecs.open(file_path, mode='r', encoding='utf-8') as f:
        lines = f.read()
    return lines


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
    if not is_exist_file(file_path):
        return {}
    with codecs.open(file_path, mode='r', encoding='utf-8') as file:
        obj = json.load(file)
    return obj


def dump_json(file_path, dump_data):
    with codecs.open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(dump_data, file, indent=2, ensure_ascii=False)


def load_yaml(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        obj = yaml.safe_load(file)
    return obj
