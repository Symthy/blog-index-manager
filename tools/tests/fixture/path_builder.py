import os


def build_test_data_path(path: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_path = '../test_data/' + path
    return os.path.join(current_dir, test_data_path.replace('/', os.sep))


def test_root_dir_path() -> str:
    # test root: tools/tests
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir_path = os.path.join(current_dir, '..')
    return tests_dir_path.replace('/', os.sep)
