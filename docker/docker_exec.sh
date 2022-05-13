#!/bin/bash

# constant
DOCKER_IMAGE_NAME="docs-manager:latest"
DOCKER_CONTAINER_NAME="docs-manager"

docker_compose_cmd=`which docker-compose`
docker_cmd=`which docker`

function validate_docker_command() {
  if [ -z "${docker_compose_cmd}" -a -z "${docker_cmd}" ]; then
    echo "[Error] Nothing docker command."
    exit 1
  fi
}

function build_docker_image() {
  docker_image=`docker image ls -q ${DOCKER_IMAGE_NAME}`
  if [ ! -z "${docker_image}" ]; then
    return
  fi
  echo "=== START - docker image build ==="
  if [ -n "${docker_compose_cmd}" ]; then
    docker-compose build
  else
    docker build -f docker/Dockerfile -t "${DOCKER_IMAGE_NAME}" .
  fi
  echo "=== END - docker image build ==="
  echo
}

function run_docker_container() {
  args="-"
  if [ $# -ge 1 ]; then
    args=$@
  fi
  build_docker_image
  echo "=== START - docker container run ==="
  if [ -n "${docker_compose_cmd}" ]; then
    OPTION="${args}" docker-compose up -d
    sleep 1  # wait container stop
    show_docker_logs
    docker-compose rm -f "${DOCKER_CONTAINER_NAME}"
  else
    docker run -d -t -v `pwd`:/work --rm --name "${DOCKER_CONTAINER_NAME}" "${DOCKER_IMAGE_NAME}" "${args}"
  fi
  echo "=== END - docker container run ==="
  echo
}

function stop_docker_container() {
  # container stop
  echo "=== START - docker container stop ==="
  if [ -n "${docker_compose_cmd}" ]; then
    docker-compose down
  else
    stop_result=`docker stop "${DOCKER_CONTAINER_NAME}"`
    if [ $? -eq 0 ]; then
      echo "container stop success"
    else
      echo "${stop_result}"
    fi
  fi
  echo "=== END - docker container stop ==="
  echo
}

function show_docker_logs() {
  echo
  echo "--- tool logs"
  docker logs "${DOCKER_CONTAINER_NAME}"
  echo "---"
  echo
}