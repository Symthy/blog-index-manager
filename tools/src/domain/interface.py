from abc import ABC, abstractmethod
from typing import List, Optional


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
    @abstractmethod
    def dump_data(self, dump_file_path: str):
        pass


class IEntries(IConvertibleMarkdownLines, ABC):
    @abstractmethod
    def get_entries(self) -> List[IEntry]:
        pass

    @abstractmethod
    def dump_all_data(self, dump_file_path: str):
        pass
