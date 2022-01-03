import codecs
import configparser
import json
from typing import List

import yaml

from file.blog_config import BlogConfig
from file.category_group_def import CategoryGroupDef


def read_blog_config(config_path):
    conf_parser = configparser.ConfigParser()
    conf_parser.read(config_path)
    return BlogConfig(conf_parser)


def read_text_file(file_path: str):
    try:
        with codecs.open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            lines_exclusion_comment = list(filter(lambda line: not line.startswith('#'), lines))
            return [line.replace('\n', '') for line in lines_exclusion_comment]
    except Exception as e:
        print(f'[Warning] Invalid {file_path}, read failure:', e)
        return []


def write_text_file(file_path, lines: List[str]):
    try:
        with codecs.open(file_path, mode='w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print(f'[Warning] Invalid {file_path}, write failure:', e)
        return []


def load_json(file_path):
    with codecs.open(file_path, mode='r', encoding='utf-8') as file:
        obj = json.load(file)
    return obj


def dump_json(file_path, dump_data):
    with codecs.open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(dump_data, file, indent=2, ensure_ascii=False)


def load_category_group_def_yaml() -> CategoryGroupDef:
    CATEGORY_GROUP_YAML_PATH = '../definitions/category_group.yml'
    json_data = load_yaml(CATEGORY_GROUP_YAML_PATH)  # return list
    return CategoryGroupDef(json_data)


def load_yaml(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        obj = yaml.safe_load(file)
    return obj

# def write_md_file(file_path: str, lines: List[str]):
