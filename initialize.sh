#!/bin/bash -eu

root_path=$(dirname $(readlink -f $0))
source "${root_path}/docker/docker_exec.sh"

pushd ${root_path} > /dev/null

if [ ! -e "${root_path}/conf/blog.conf" ]; then
  cp "${root_path}/conf/blog.conf.model" "${root_path}/conf/blog.conf"
fi

run_docker_container "-init"

popd > /dev/null
