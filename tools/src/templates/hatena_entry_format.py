from datetime import datetime
from xml.sax.saxutils import escape

from file.blog_config import BlogConfig
from ltime.time_resolver import resolve_entry_current_time

SUMMARY_PAGE_TITLE = ""


def get_summary_page_title() -> str:
    return "Knowledge Index (記事一覧)"


ENTRY_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{title}</title>
  <author><name>{author}</name></author>
  <content type="text/x-markdown">{content}</content>
  <updated>{update_time}</updated>
  <category term="{category}" />
  <app:control>
    <app:draft>{draft}</app:draft>
  </app:control>
</entry>"""


def build_hatena_entry_xml_body(blog_conf: BlogConfig, title: str, category: str, content: str) -> str:
    current_time = datetime.now()
    entry_xml = ENTRY_TEMPLATE.format(
        title=title,
        author=blog_conf.hatena_id,
        content=replace_xml_escape(content),
        update_time=resolve_entry_current_time(),
        category=category,
        draft='yes'  # yes or no
    )
    return entry_xml


def replace_xml_escape(content: str) -> str:
    # entities = {
    #     '\"': '&quot;',
    #     '\'': '&apos;',
    # }
    return escape(content)  # escape: <, &, >,
