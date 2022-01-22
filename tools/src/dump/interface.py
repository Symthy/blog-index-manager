from abc import ABC
from typing import TypeVar, Generic

from domain.blog.blog_entry import BlogEntries, BlogEntry
from domain.doc.doc_entry import DocEntries, DocEntry

TM = TypeVar('TM', DocEntries, BlogEntries)
TS = TypeVar('TS', DocEntry, BlogEntry)


class IDumpEntriesAccessor(ABC, Generic[TM]):
    def load_entries(self) -> TM:
        pass

    def save_entries(self, entries: TM):
        pass


class IDumpEntryAccessor(ABC, Generic[TS]):
    def load_entry(self, entry_id: str) -> TS:
        pass

    def save_entry(self, entry: TS):
        pass
