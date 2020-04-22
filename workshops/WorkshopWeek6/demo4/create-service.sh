#!/usr/bin/env bash

echo "docker-machine ssh manager docker service create --replicas 3 -p 8083:80 --name nginx nginx:alpine"

docker-machine ssh manager docker service create --replicas 3 -p 8083:80 --name nginx nginx:alpine
