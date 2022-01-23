# relative path
DATA_DIR_PATH = './tools/data/'

HATENA_BLOG_ENTRY_DUMP_DIR = DATA_DIR_PATH + 'hatena_entry_data/'
HATENA_BLOG_ENTRY_LIST_PATH = DATA_DIR_PATH + 'hatena_entry_list.json'
HATENA_BLOG_ENTRY_INDEX_RESULT_PATH = DATA_DIR_PATH + 'hatena_entry_grouping_result.md'

LOCAL_DOCS_ENTRY_DUMP_DIR = DATA_DIR_PATH + 'local_entry_data/'
LOCAL_DOCS_ENTRY_LIST_PATH = DATA_DIR_PATH + 'local_entry_list.json'
LOCAL_DOCS_ENTRY_GROUPING_PATH = DATA_DIR_PATH + 'local_entry_grouping.json'

HATENA_BLOG_TO_DOC_ENTRY_DICTIONARY_PATH = DATA_DIR_PATH + 'hatena_blog_to_doc_dict.json'
LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH = './SUMMARY.md'

WORK_DIR_PATH = './work/'

DOCS_DIR_PATH = './docs/'

BACKUP_DIR_PATH = './backup/'

CONF_DIR_PATH = './conf/'
BLOG_CONF_PATH = CONF_DIR_PATH + 'blog.conf'

EXCLUDE_ENTRY_IDS_TXT_PATH = CONF_DIR_PATH + 'exclude_entry_ids.txt'
CATEGORY_GROUP_YAML_PATH = CONF_DIR_PATH + 'category_group_def.yml'

ID_FILE_NAME_HEADER = '.id_'
CATEGORY_FILE_NAME = 'category.txt'
DOCS_DIR_PATH_TEMP_FILE = 'master_path_temp'
DOC_IMAGES_DIR_NAME = 'images/'
DOC_TITLE_MAX_LENGTH = 50

# category_group.yml に 定義していないCategory もしくは Category未設定 の doc/blog を紐づけるための Group
NON_CATEGORY_GROUP_NAME = 'Others'
