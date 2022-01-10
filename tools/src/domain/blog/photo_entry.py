from typing import Dict, List, Optional


class PhotoEntry:
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_SYNTAX = 'syntax'
    FIELD_IMAGE_URL = 'image_url'

    def __init__(self, image_filename: str, entry_id: str, title: str, syntax: str, image_url: str):
        self.__image_filename = image_filename
        self.__id = entry_id
        self.__title = title
        self.__syntax = syntax
        self.__image_url = image_url

    @property
    def image_filename(self) -> str:
        return self.__image_filename

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def syntax(self) -> str:
        return self.__syntax

    @property
    def image_url(self):
        return self.__image_url

    def build_dump_data(self) -> Dict[str, Dict[str, str]]:
        return {
            self.__image_filename: {
                PhotoEntry.FIELD_ID: self.__id,
                PhotoEntry.FIELD_TITLE: self.__title,
                PhotoEntry.FIELD_SYNTAX: self.__syntax,
                PhotoEntry.FIELD_IMAGE_URL: self.__image_url
            }
        }

    @classmethod
    def init_from_dump_data(cls, image_filename: str, dump_data: Dict[str, str]):
        return PhotoEntry(
            image_filename,
            dump_data[PhotoEntry.FIELD_ID],
            dump_data[PhotoEntry.FIELD_TITLE],
            dump_data[PhotoEntry.FIELD_SYNTAX],
            dump_data[PhotoEntry.FIELD_IMAGE_URL]
        )


class PhotoEntries:
    def __init__(self, images_dict: Optional[Dict[str, PhotoEntry]] = None):
        # key: image file name
        self.__filename_to_photo_entry: Dict[str, PhotoEntry] = {} if images_dict is None else images_dict

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

    def build_dump_data(self) -> Dict[str, Dict[str, str]]:
        dump_data = {}
        for entry in self.entry_list:
            dump_data |= entry.build_dump_data()
        return dump_data

    @classmethod
    def init_from_dump_data(cls, dump_data: Dict[str, Dict[str, str]]):
        photo_entry_dict = {}
        for image_filename, entry_data in dump_data.items():
            if len(entry_data) > 0:
                photo_entry_dict[image_filename] = PhotoEntry.init_from_dump_data(image_filename, entry_data)
        return PhotoEntries(photo_entry_dict)
