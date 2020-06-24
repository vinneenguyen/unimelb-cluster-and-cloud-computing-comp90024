#!/usr/bin/env bash

echo "docker-machine ssh manager docker service scale nginx=1"

docker-machine ssh manager docker service scale nginx=1
