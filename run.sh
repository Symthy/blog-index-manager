#!/bin/bash -eu

root_path=$(dirname $(readlink -f $0))

pushd ${root_path} > /dev/null
source ${root_path}/docker/docker_exec.sh

# echo "=== python version ==="
# docker exec -it "${DOCKER_CONTAINER_NAME}" python --version
# echo "======================"

run_docker_container $@

