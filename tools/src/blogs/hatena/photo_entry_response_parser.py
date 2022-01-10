import xml.etree.ElementTree as ET

from domain.blog.photo_entry import PhotoEntry


def print_xml_children(root: ET.Element):
    """
    for debug
    """
    for child in root:
        print(child.tag)


def parse_photo_entry_xml(xml_string: str) -> PhotoEntry:
    root = ET.fromstring(xml_string)
    print_xml_children(root)
    return
