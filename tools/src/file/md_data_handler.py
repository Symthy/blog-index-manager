from typing import List

from domain.interface import IConvertibleMarkdownLines


def join_lines(lines: List[str]) -> str:
    data = ''
    for line in lines:
        data = data + line + '\n'
    return data



