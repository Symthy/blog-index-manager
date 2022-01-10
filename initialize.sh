#!/bin/bash -eu

root_dir_path=$(dirname $(readlink -f $0))

pushd ${root_dir_path} > /dev/null

tool_script_path="${root_dir}/tools/src/main.py"

python3 ${tool_script_path} -init

copy ./conf/blog.conf.model ./conf/blog.conf

popd