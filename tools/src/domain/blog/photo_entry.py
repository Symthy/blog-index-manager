from typing import Dict, List, Optional


class PhotoEntry:
    def __init__(self, image_filename: str, entry_id: str, syntax: str, image_url: str):
        self.__image_filename = image_filename
        self.__id = entry_id
        self.__syntax = syntax
        self.__image_url = image_url

    @property
    def id(self) -> str:
        return self.__id

    @property
    def syntax(self) -> str:
        return self.__syntax

    @property
    def image_url(self):
        return self.__image_url

    def build_dump_data(self):
        return {
            self.__image_filename: {
                'id': self.__id,
                'syntax': self.__syntax,
                'image_url': self.__image_url
            }
        }


class PhotoEntries:
    def __init__(self):
        self.__filename_to_photo_entry: Dict[str, PhotoEntry] = {}

    @property
    def entry_list(self) -> List[PhotoEntry]:
        return list(self.__filename_to_photo_entry.values())

    def is_exist(self, image_filename: str) -> bool:
        return image_filename in self.__filename_to_photo_entry

    def get_entry(self, image_filename: str) -> Optional[PhotoEntry]:
        if not self.is_exist(image_filename):
            return None
        return self.__filename_to_photo_entry[image_filename]

    def get_syntax(self, image_filename: str) -> Optional[str]:
        entry = self.get_entry(image_filename)
        if entry is None:
            return None
        return entry.syntax

    def build_dump_data(self) -> List[Dict[str, Dict[str, str]]]:
        return [e.build_dump_data() for e in self.entry_list]
