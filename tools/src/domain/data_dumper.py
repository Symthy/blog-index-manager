from domain.interface import IDumpDataBuilder
from file.file_accessor import load_json, dump_json
from file.files_operator import is_exist_file


def resolve_dump_field_data(entry, dump_data, field_name) -> str:
    if dump_data is None:
        return getattr(entry, field_name)
    if field_name in dump_data:
        return dump_data[field_name]
    return getattr(entry, field_name)


def dump_entry_data(builder: IDumpDataBuilder, dump_file_path: str):
    exist_file_data = None
    if is_exist_file(dump_file_path):
        exist_file_data = load_json(dump_file_path)
    dump_data = builder.build_dump_data(exist_file_data)
    dump_json(dump_file_path, dump_data)
