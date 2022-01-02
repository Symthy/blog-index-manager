from typing import List


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
        self.__grouping_categories: List[GroupingCategories] = []
        self.__all_group_and_category: List[str] = []
        for record in json_data:
            if isinstance(record, str):
                self.__grouping_categories.append(GroupingCategories(record))
                self.__all_group_and_category.append(record)
            elif isinstance(record, dict):
                for group, categories in record.items():
                    self.__grouping_categories.append(GroupingCategories(group, categories))
                    self.__all_group_and_category.append(group)
                    self.__all_group_and_category.extend(categories)

    @property
    def grouping_categories(self) -> List[GroupingCategories]:
        return self.__grouping_categories

    def is_non_exist_group_or_category(self, name) -> bool:
        return not name in self.__all_group_and_category

    def print_data(self):
        # for debug
        for gc in self.__grouping_categories:
            gc.print_data()
