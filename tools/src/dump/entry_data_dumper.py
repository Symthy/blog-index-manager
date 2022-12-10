from typing import Union, List

from domain.interface import IDumpDataBuilder, IEntry
from files.file_accessor import load_json, dump_json
from files.files_operator import is_exist_file


def resolve_dump_str_field(entry: IEntry, dump_data, field_name: Union[str, List[str]]):
    # Todo: refactor
    new_field_data = getattr(entry, field_name)
    if dump_data is None:
        return new_field_data
    if new_field_data is None or len(new_field_data) == 0:
        if field_name not in dump_data:
            return ''
        return dump_data[field_name]
    return new_field_data


def resolve_dump_bool_field(entry: IEntry, dump_data, field_name: str) -> bool:
    new_field_data = getattr(entry, field_name)
    if new_field_data is not None:
        return new_field_data
    if dump_data is None or field_name not in dump_data:
        return False
    return dump_data[field_name]


def dump_entry_data(builder: IDumpDataBuilder, dump_file_path: str):
    exist_file_data = None
    if is_exist_file(dump_file_path):
        exist_file_data = load_json(dump_file_path)
    dump_data = builder.build_dump_data(exist_file_data)
    dump_json(dump_file_path, dump_data)
