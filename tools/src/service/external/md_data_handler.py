from typing import List

from domain.interface import IConvertibleMarkdownLines


def join_lines(lines: List[str]) -> str:
    data = ''
    for line in lines:
        data = data + line + '\n'
    return data


def print_md_lines(data: IConvertibleMarkdownLines):
    # for debug
    print(join_lines(data.convert_md_lines()))
