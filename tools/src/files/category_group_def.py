from typing import List, Dict

from common.constant import NON_CATEGORY_GROUP_NAME


class GroupingCategories:
    def __init__(self, group_name, categories=None):
        if categories is None:
            categories = []
        self.__group_name: str = group_name
        self.__categories: List[str] = categories

    @property
    def group_name(self):
        return self.__group_name

    @property
    def categories(self):
        return self.__categories

    def print_data(self):
        print(f'{self.__group_name}: {self.__categories}')


class CategoryGroupDef:
    def __init__(self, json_data: List):
        self.__group_to_categories: Dict[str, List[str]] = {}
        self.__grouping_categories: Dict[str, GroupingCategories] = {}
        self.__all_group_and_category: List[str] = []
        self.__category_to_group = {}  # key: category only. don't include group in key
        for json_field_group in json_data:
            if isinstance(json_field_group, str):
                self.__group_to_categories[json_field_group] = []
                self.__grouping_categories[json_field_group] = GroupingCategories(json_field_group)
                self.__all_group_and_category.append(json_field_group)
            elif isinstance(json_field_group, dict):
                for group, categories in json_field_group.items():
                    self.__group_to_categories[group] = categories
                    self.__grouping_categories[group] = GroupingCategories(group, categories)
                    self.__all_group_and_category.append(group)
                    self.__all_group_and_category.extend(categories)
                    for category in categories:
                        self.__category_to_group[category] = group

    @property
    def groups(self) -> List[str]:
        return list(self.__group_to_categories.keys())

    @property
    def categories(self) -> List[str]:
        return list(self.__category_to_group.keys())

    @property
    def grouping_categories(self) -> List[GroupingCategories]:
        return [self.__grouping_categories[group] for group in self.groups]

    def has_group_or_category(self, name) -> bool:
        return name in self.__all_group_and_category

    def has_group_case_insensitive(self, name) -> bool:
        for group in self.groups:
            if name.lower() == group.lower():
                return True
        return False

    def has_group(self, name):
        return name in self.groups

    def has_category(self, name):
        return name in self.categories

    def get_categories(self, group: str) -> List[str]:
        return self.__grouping_categories[group].categories

    def get_belongs_group(self, category: str) -> str:
        if category in self.__category_to_group:
            return self.__category_to_group[category]
        if category in self.groups:
            return category
        return NON_CATEGORY_GROUP_NAME

    def print_data(self):
        # for debug
        for group in self.groups:
            self.__grouping_categories[group].print_data()
