from typing import List, Dict


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
        self.__groups: List[str] = []
        self.__grouping_categories: Dict[str, GroupingCategories] = {}
        self.__all_group_and_category: List[str] = []
        self.__category_to_group = {}
        for json_field in json_data:
            if isinstance(json_field, str):
                self.__groups.append(json_field)
                self.__grouping_categories[json_field] = GroupingCategories(json_field)
                self.__all_group_and_category.append(json_field)
            elif isinstance(json_field, dict):
                for group, categories in json_field.items():
                    self.__groups.append(group)
                    self.__grouping_categories[group] = GroupingCategories(group, categories)
                    self.__all_group_and_category.append(group)
                    self.__all_group_and_category.extend(categories)
                    for category in categories:
                        self.__category_to_group[category] = group

    @property
    def groups(self) -> List[str]:
        return self.__groups

    @property
    def grouping_categories(self) -> List[GroupingCategories]:
        return [self.__grouping_categories[group] for group in self.__groups]

    def is_non_exist_group_or_category(self, name) -> bool:
        return not name in self.__all_group_and_category

    def has_group(self, name):
        return name in self.__groups

    def get_categories(self, group: str) -> List[str]:
        return self.__grouping_categories[group].categories

    def get_belongs_group(self, category: str):
        return self.__category_to_group[category]

    def print_data(self):
        # for debug
        for group in self.__groups:
            self.__grouping_categories[group].print_data()
