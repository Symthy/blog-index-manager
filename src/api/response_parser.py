import xml.etree.ElementTree as ET

from domain.blog_entry import BlogEntries, BlogEntry


def parse_blog_entries_xml(root: ET.Element) -> BlogEntries:
    tag_head = root.tag[:-len('feed')]  # tag : {http://www.w3.org/2005/Atom}feed
    blog_entries = BlogEntries()
    for entry in root.iter(tag_head + 'entry'):
        blog_entry = parse_blog_entry_xml(entry, tag_head)
        blog_entries.add_entry(blog_entry)
    return blog_entries


def parse_blog_entry_xml(root: ET.Element, tag_head: str) -> BlogEntry:
    id = root.find(tag_head + 'id').text
    title = root.find(tag_head + 'title').text
    content = root.find(tag_head + 'content').text
    updated = root.find(tag_head + 'updated').text
    url = ''
    categories = []
    for link in root.iter(tag_head + 'link'):
        if link.attrib['rel'] == 'alternate':
            url = link.attrib['href']
            break
    for category in root.iter(tag_head + 'category'):
        categories.append(category.attrib['term'])
    return BlogEntry(id, title, content, url, updated, categories)
