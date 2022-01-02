from configparser import ConfigParser

CONF_SECTION_HATENA = 'HATENA'
CONF_KEY_HATENA_ID = 'HATENA_ID'
CONF_KEY_BLOG_ID = 'BLOG_ID'
CONF_KEY_API_KEY = 'API_KEY'


class BlogConfig:
    def __init__(self, conf: ConfigParser):
        self.__hatena_id = conf.get(CONF_SECTION_HATENA, CONF_KEY_HATENA_ID)
        self.__blog_id = conf.get(CONF_SECTION_HATENA, CONF_KEY_BLOG_ID)
        self.__api_key = conf.get(CONF_SECTION_HATENA, CONF_KEY_API_KEY)

    @property
    def hatena_id(self):
        return self.__hatena_id

    @property
    def blog_id(self):
        return self.__blog_id

    @property
    def api_key(self):
        return self.__api_key
