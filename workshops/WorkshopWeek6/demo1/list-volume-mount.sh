#!/bin/bash

echo "docker exec -ti nginx-volume sh -c \"ls -ltr /usr/share/nginx/html\""

docker exec -ti nginx-volume sh -c "ls -ltr /usr/share/nginx/html"

echo ""
echo ""
echo ""
echo "docker exec -ti nginx-bind sh -c \"ls -ltr /usr/share/nginx/html\""

docker exec -ti nginx-bind sh -c "ls -ltr /usr/share/nginx/html"
