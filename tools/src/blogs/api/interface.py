from abc import ABC, abstractmethod
from typing import Optional

from domain.blog.blog_entry import BlogEntry, BlogEntries
from domain.blog.photo_entry import PhotoEntry


class IBlogApiExecutor(ABC):
    @abstractmethod
    def execute_get_blog_entry_api(self, entry_id: str) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def execute_get_all_blog_entries_api(self) -> BlogEntries:
        pass

    @abstractmethod
    def execute_register_blog_entry_api(self, title: str, category: str, content: str,
                                        is_draft: bool) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def execute_update_blog_summary_page(self, content: str) -> bool:
        pass

    @abstractmethod
    def execute_update_blog_entry_api(self, entry_id: str, title: str, category: str,
                                      content: str, is_draft: bool) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def execute_get_photo_entry_api(self, entry_id: str) -> Optional[PhotoEntry]:
        pass

    @abstractmethod
    def execute_register_photo_entry_api(self, image_file_path: str) -> Optional[PhotoEntry]:
        pass

    @abstractmethod
    def execute_update_photo_entry_api(self, image_file_path: str, photo_entry: PhotoEntry) -> Optional[PhotoEntry]:
        pass
