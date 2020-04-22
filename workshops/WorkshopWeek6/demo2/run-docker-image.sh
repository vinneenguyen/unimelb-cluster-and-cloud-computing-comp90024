#!/bin/bash

echo ""
echo ""
echo ""
echo "docker run --name demo2-1 -p 8080:80 -d demo2"

docker run --name demo2-1 -p 8080:80 -d demo2

echo ""
echo ""
echo ""
echo "docker run --name demo2-2 -p 8081:80 -e WELCOME_STRING=\"COMP90024\" -d demo2"

docker run --name demo2-2 -p 8081:80 -e WELCOME_STRING=COMP90024 -e TEST=hello -d demo2