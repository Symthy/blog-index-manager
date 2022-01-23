from xml.sax.saxutils import escape

from ltime.time_resolver import resolve_entry_current_time

SUMMARY_PAGE_TITLE = "Knowledge Index (記事一覧)"


def get_summary_page_title() -> str:
    return SUMMARY_PAGE_TITLE


__BLOG_ENTRY_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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


def __replace_xml_escape(content: str) -> str:
    # entities = {
    #     '\"': '&quot;',
    #     '\'': '&apos;',
    # }
    return escape(content)  # escape: <, &, >,


def build_hatena_blog_entry_xml_body(hatena_id: str, title: str, category: str, content: str,
                                     is_draft: bool = True) -> str:
    entry_xml = __BLOG_ENTRY_TEMPLATE.format(
        title=title,
        author=hatena_id,
        content=__replace_xml_escape(content),
        update_time=resolve_entry_current_time(),
        category=category,
        draft='yes' if is_draft else 'no'  # yes or no
    )
    return entry_xml


def get_blog_summary_index_template() -> str:
    return """本ページは投稿記事一覧です。 (自動更新)

{md_lines}
    """


def get_blog_entry_template() -> str:
    return """[:contents]

{content}
"""


__PHOTO_LIFE_POST_ENTRY_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://purl.org/atom/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <title>{title}</title>
  <content mode="base64" type="{content_type}">{content}</content>
  <dc:subject>Hatena Blog</dc:subject>
</entry>
"""


def build_hatena_photo_entry_post_xml_body(title: str, content_type: str, b64_pic_data: str) -> str:
    entry_xml = __PHOTO_LIFE_POST_ENTRY_TEMPLATE.format(
        title=title,
        content_type=content_type,
        content=b64_pic_data
    )
    return entry_xml
