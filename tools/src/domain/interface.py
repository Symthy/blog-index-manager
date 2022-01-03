from abc import ABC, abstractmethod
from typing import List


class IConvertibleMarkdownData(ABC):
    @abstractmethod
    def convert_md_lines(self) -> List[str]:
        pass
