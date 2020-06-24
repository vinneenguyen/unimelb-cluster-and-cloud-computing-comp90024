#!/bin/bash

echo "docker volume create --name htdocs"
docker volume create --name htdocs


echo ""
echo ""
echo ""
echo "docker run --name nginx-volume -p 8080:80 -v htdocs:/usr/share/nginx/html -d nginx"

docker run --name nginx-volume -p 8080:80 -v htdocs:/usr/share/nginx/html -d nginx

echo ""
echo ""
echo ""
echo "docker run --name nginx-bind -p 8081:80 -v $(pwd)/htdocs:/usr/share/nginx/html -d nginx"

docker run --name nginx-bind -p 8081:80 -v $(pwd)/htdocs:/usr/share/nginx/html -d nginx
