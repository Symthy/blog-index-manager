import xml.etree.ElementTree as ET

from domain.blog.photo_entry import PhotoEntry
from ltime.time_resolver import get_current_datetime


def print_xml_children(root: ET.Element):
    """
    for debug
    """
    for child in root:
        print(child.tag)


__PHOTO_ENTRY_XML_NAMESPACE = '{http://purl.org/atom/ns#}'
__PHOTO_ENTRY_HATENA_XML_NAMESPACE = '{http://www.hatena.ne.jp/info/xmlns#}'


def parse_photo_entry_xml(xml_string: str, image_filename: str) -> PhotoEntry:
    root = ET.fromstring(xml_string)
    # print_xml_children(root)
    entry_id = root.find(__PHOTO_ENTRY_XML_NAMESPACE + 'id').text.rsplit('-', 1)[1]
    syntax = root.find(__PHOTO_ENTRY_HATENA_XML_NAMESPACE + 'syntax').text
    image_url = root.find(__PHOTO_ENTRY_HATENA_XML_NAMESPACE + 'imageurl').text
    # don't know if the API response includes the update time.
    updated_datetime = get_current_datetime()
    return PhotoEntry(image_filename, entry_id, syntax, image_url, updated_datetime)
