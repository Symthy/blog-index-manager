import sys
from typing import List

from blogs.api.interface import IBlogApiExecutor
from command.options_controller import execute_command


def show_hatena_blog_entry(api_executor: IBlogApiExecutor, entry_id):
    # for debug
    blog_entry_opt = api_executor.execute_get_blog_entry_api(entry_id)
    if blog_entry_opt is None:
        print(f'[Error] Nothing entry: {entry_id}')
        return
    print(blog_entry_opt.content)


def show_hatena_photo_entry(api_executor: IBlogApiExecutor, entry_id):
    # for debug
    photo_entry_opt = api_executor.execute_get_photo_entry_api(entry_id)
    if photo_entry_opt is None:
        print(f'[Error] Nothing entry: {entry_id}')
        return
    print(photo_entry_opt.build_dump_data())


def main(args: List[str], is_debug: bool):
    arg_str = ' '.join(args[1:])
    print(f'tool run. (specified options: {arg_str})\n')
    execute_command(args)


IS_DEBUG = False
main(sys.argv, IS_DEBUG)
