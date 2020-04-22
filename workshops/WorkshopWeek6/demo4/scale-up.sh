#!/usr/bin/env bash

echo "docker-machine ssh manager docker service scale nginx=6"

docker-machine ssh manager docker service scale nginx=6
