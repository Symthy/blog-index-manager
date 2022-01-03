import xml.etree.ElementTree as ET
from datetime import datetime

from domain.blog_entry import BlogEntries, BlogEntry


def parse_blog_entries_xml(root: ET.Element) -> BlogEntries:
    tag_head = root.tag[:-len('feed')]  # tag example: {http://www.w3.org/2005/Atom}feed
    blog_entries = BlogEntries()
    for entry in root.iter(tag_head + 'entry'):
        blog_entry = parse_blog_entry_xml(entry, tag_head)
        blog_entries.add_entry(blog_entry)
    return blog_entries


def parse_blog_entry_xml(root: ET.Element, tag_head: str) -> BlogEntry:
    # id example: tag:blog.hatena.ne.jp,2013:blog-Sympathia-17680117126980108518-13574176438048806685
    # entry id is last sequence
    entry_id = root.find(tag_head + 'id').text.rsplit('-', 1)[1]

    title = root.find(tag_head + 'title').text
    content = root.find(tag_head + 'content').text

    updated_opt = root.find(tag_head + 'updated')
    last_update_time = None
    if updated_opt is not None:
        # format: 2013-09-02T11:28:23+09:00
        last_update_time = datetime.strptime(updated_opt.text, "%Y-%m-%dT%H:%M:%S%z")
    app_edited_opt = root.find(tag_head + 'app\\:edited')
    if app_edited_opt is not None:
        # format: 2013-09-02T11:28:23+09:00
        app_edited_time = datetime.strptime(app_edited_opt.text, "%Y-%m-%dT%H:%M:%S%z")
        if last_update_time < app_edited_time:
            last_update_time = app_edited_time

    url = ''
    for link in root.iter(tag_head + 'link'):
        if link.attrib['rel'] == 'alternate':
            url = link.attrib['href']
            break
    api_url = ''
    for link in root.iter(tag_head + 'link'):
        if link.attrib['rel'] == 'edit':
            api_url = link.attrib['href']
            break
    categories = []
    for category in root.iter(tag_head + 'category'):
        categories.append(category.attrib['term'])
    return BlogEntry(entry_id, title, content, url, api_url, last_update_time, categories)
