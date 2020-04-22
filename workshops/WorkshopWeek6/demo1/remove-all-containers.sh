#!/bin/bash

echo "docker rm -f \$(docker ps -aq)"

docker rm -f $(docker ps -aq)