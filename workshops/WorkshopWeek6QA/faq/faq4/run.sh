#!/usr/bin/env bash

docker build -t nginx-test:latest .

docker run --name test1 -p 180:80 -d nginx-test:latest

docker run --name test2 -P -d nginx-test:latest

docker run --name test3 -P -d nginx:latest

docker ps -a
