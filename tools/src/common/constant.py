# relative path
OUT_DIR_PATH = './tools/out/'

HATENA_BLOG_ENTRY_DUMP_DIR = OUT_DIR_PATH + 'hatena_entry_data/'
HATENA_BLOG_ENTRY_LIST_PATH = OUT_DIR_PATH + 'hatena_entry_list.json'
HATENA_BLOG_ENTRY_INDEX_RESULT_PATH = OUT_DIR_PATH + 'hatena_entry_index_result.md'

LOCAL_DOCS_ENTRY_DUMP_DIR = OUT_DIR_PATH + 'local_entry_data/'
LOCAL_DOCS_ENTRY_LIST_PATH = OUT_DIR_PATH + 'local_entry_list.json'
LOCAL_DOCS_ENTRY_GROUPING_PATH = OUT_DIR_PATH + 'local_entry_grouping.json'

HATENA_BLOG_TO_DOC_ENTRY_DICTIONARY_PATH = OUT_DIR_PATH + 'hatena_blog_to_doc_dict.json'
LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH = './SUMMARY.md'

WORK_DIR_PATH = './work/'

DOCS_DIR_PATH = './docs/'

BACKUP_DIR_PATH = './backup/'

CONF_DIR_PATH = './conf/'
BLOG_CONF_PATH = CONF_DIR_PATH + 'blog.conf'

DEFINITIONS_DIR_PATH = './tools/definitions/'
EXCLUDE_ENTRY_IDS_TXT_PATH = DEFINITIONS_DIR_PATH + 'exclude_entry_ids.txt'
CATEGORY_GROUP_YAML_PATH = DEFINITIONS_DIR_PATH + 'category_group.yml'

ID_FILE_NAME_HEADER = '.id_'
CATEGORY_FILE_NAME = 'category.txt'
DOC_IMAGES_DIR_NAME = 'images'
DOC_TITLE_MAX_LENGTH = 50

# category_group.yml に 定義していないCategory もしくは Category未設定 の doc/blog を紐づけるための Group
NON_CATEGORY_GROUP_NAME = 'Others'
