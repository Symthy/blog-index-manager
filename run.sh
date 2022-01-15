#!/bin/bash -eu

root_dir_path=$(dirname $(readlink -f $0))

pushd ${root_dir_path} > /dev/null

tool_script_path="${root_dir_path}/tools/src/main.py"

python ${tool_script_path} $@
