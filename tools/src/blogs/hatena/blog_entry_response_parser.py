import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

from common.constant import EXCLUDE_ENTRY_IDS_TXT_PATH
from domain.blog.blog_entry import BlogEntries, BlogEntry
from file.blog_config import BlogConfig
from file.file_accessor import read_text_file


def print_xml_children(root: ET.Element):
    """
    for debug
    """
    for child in root:
        print(child.tag)


def get_tag_head(root: ET.Element, root_tag: str = 'feed') -> str:
    tag_head = root.tag[:-len(root_tag)]  # tag example: {http://www.w3.org/2005/Atom}feed
    return tag_head


def get_next_page_url(xml_string: str) -> Optional[str]:
    url = None
    root = ET.fromstring(xml_string)
    for link in root.iter(get_tag_head(root) + 'link'):
        if link.attrib['rel'] == 'next':
            url = link.attrib['href']
            break
    return url


def parse_blog_entries_xml(xml_string: str, blog_config: BlogConfig) -> BlogEntries:
    root = ET.fromstring(xml_string)
    # print_xml_children(root)
    tag_head = get_tag_head(root)
    blog_entries = BlogEntries()
    exclude_ids = read_text_file(EXCLUDE_ENTRY_IDS_TXT_PATH)
    exclude_ids.append(blog_config.summary_entry_id)  # exclude summary entry index page
    for entry in root.iter(tag_head + 'entry'):
        # print_xml_children(entry)
        blog_entry = __parse_blog_entry_xml(entry, tag_head, exclude_ids)
        if blog_entry is not None:
            blog_entries.add_entry(blog_entry)
    return blog_entries


def parse_blog_entry_xml(xml_string: str) -> BlogEntry:
    root = ET.fromstring(xml_string)
    tag_head = get_tag_head(root, 'entry')
    return __parse_blog_entry_xml(root, tag_head, [])


def __parse_blog_entry_xml(entry_node: ET.Element, tag_head: str, exclude_ids: List[str]) -> Optional[BlogEntry]:
    # id example: tag:blog.hatena.ne.jp,2013:blog-Sympathia-17680117126980108518-13574176438048806685
    # entry id is last sequence
    entry_id = entry_node.find(tag_head + 'id').text.rsplit('-', 1)[1]
    if entry_id in exclude_ids:
        return None

    title = entry_node.find(tag_head + 'title').text
    content = ''
    for cont in entry_node.iter(tag_head + 'content'):
        if cont.attrib['type'] == 'text/x-markdown':
            content = cont.text
            break

    updated_opt = entry_node.find(tag_head + 'updated')
    last_update_time = None
    if updated_opt is not None:
        # format: 2013-09-02T11:28:23+09:00
        last_update_time = datetime.strptime(updated_opt.text, "%Y-%m-%dT%H:%M:%S%z")
    app_edited_opt = entry_node.find('{http://www.w3.org/2007/app}edited')  # app:edited
    if app_edited_opt is not None:
        # format: 2013-09-02T11:28:23+09:00
        app_edited_time = datetime.strptime(app_edited_opt.text, "%Y-%m-%dT%H:%M:%S%z")
        if last_update_time < app_edited_time:
            last_update_time = app_edited_time

    url = ''
    for link in entry_node.iter(tag_head + 'link'):
        if link.attrib['rel'] == 'alternate':
            url = link.attrib['href']
            break
    # api_url = ''
    # for link in entry_node.iter(tag_head + 'link'):
    #     if link.attrib['rel'] == 'edit':
    #         api_url = link.attrib['href']
    #         break
    categories = []
    for category in entry_node.iter(tag_head + 'category'):
        categories.append(category.attrib['term'])
    return BlogEntry(entry_id, title, content, url, last_update_time, categories)
