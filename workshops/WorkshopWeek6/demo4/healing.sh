#!/usr/bin/env bash

function pause(){
   read -p "$*"
}

echo "docker-machine ssh worker1 ps -a"

docker-machine ssh worker1 docker ps -a

pause 'Press [Enter] key to continue...'
echo ""
echo ""
echo ""
echo "docker-machine ssh worker1 docker stop \$(docker-machine ssh worker1 docker ps -aq)"

docker-machine ssh worker1 docker stop $(docker-machine ssh worker1 docker ps -aq)

pause 'Press [Enter] key to continue...'
echo ""
echo ""
echo ""
echo "docker-machine ssh worker1 docker stop \$(docker ps -aq)"

docker-machine ssh worker1 docker ps -a

sleep 5
echo ""
echo ""
echo ""
echo "docker-machine ssh worker1 docker stop \$(docker ps -aq)"

docker-machine ssh worker1 docker ps -a