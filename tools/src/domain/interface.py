from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class IDumpDataBuilder(ABC):
    @abstractmethod
    def build_dump_data(self, json_data: Optional[object] = None) -> object:
        pass


class IConvertibleMarkdownLine(ABC):
    @abstractmethod
    def convert_md_line(self) -> str:
        pass


class IConvertibleMarkdownLines(ABC):
    @abstractmethod
    def convert_md_lines(self) -> List[str]:
        pass


class IEntry(IDumpDataBuilder, IConvertibleMarkdownLine, ABC):
    @property
    def top_category(self) -> str:
        # required override
        return ''

    @abstractmethod
    def build_id_to_title(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def dump_data(self, dump_file_path: str):
        pass


class IEntries(IConvertibleMarkdownLines, ABC):
    @abstractmethod
    def get_entries(self) -> List[IEntry]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    # @abstractmethod
    # def add_entry(self, entry: IEntry):
    #     pass

    @abstractmethod
    def merge(self, entries: IEntries):
        pass

    @abstractmethod
    def dump_all_data(self, dump_file_path: str):
        pass
