#!/usr/bin/env bash

echo "docker-machine ssh manager docker service scale nginx=6"

docker-machine ssh manager docker service scale nginx=6

echo ""
echo ""
echo ""
echo "docker-machine ssh manager docker service ps nginx"

docker-machine ssh manager docker service ps nginx

echo ""
echo ""
echo ""
echo "docker-machine ssh manager docker service update --image=alwynpan/comp90024:demo1 nginx"

docker-machine ssh manager docker service update --image=alwynpan/comp90024:demo1 nginx

echo ""
echo ""
echo ""
echo "docker-machine ssh manager docker service ps nginx"

docker-machine ssh manager docker service ps nginx
