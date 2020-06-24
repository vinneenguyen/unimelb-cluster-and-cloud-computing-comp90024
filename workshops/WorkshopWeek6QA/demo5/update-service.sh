#!/usr/bin/env zsh

clear

echo "\033[0;31mdocker-machine ssh manager docker service create --replicas 3 -p 8083:80 --name nginx nginx:alpine\033[0m"

docker-machine ssh manager docker service create --replicas 3 -p 8083:80 --name nginx nginx:alpine
echo ""
echo ""

echo "\033[0;31mdocker-machine ssh manager docker service ls\033[0m"

docker-machine ssh manager docker service ls
echo ""
echo ""

echo "\033[0;31mdocker-machine ssh manager docker service ps nginx\033[0m"

docker-machine ssh manager docker service ps nginx
echo ""
echo ""

echo "Docker service \033[0;34mNginx\033[0m has been created. Press [Enter] key to continue ..."; read -k1 -s
echo ""
echo ""

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome -incognito http://192.168.99.100:8083
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome -incognito http://192.168.99.101:8083
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome -incognito http://192.168.99.102:8083

echo ""
echo ""
echo "Press [Enter] key to start \033[0;34mrolling update\033[0m ..."; read -k1 -s

echo ""
echo ""
echo "\033[0;31mdocker-machine ssh manager docker service update \033[0;34m--update-parallelism 1 --update-delay 5s\033[0m \033[0;31m--image=alwynpan/comp90024:demo1 nginx\033[0m"

echo ""
echo ""
echo "Press [Enter] key to start \033[0;34mrolling update\033[0m ..."; read -k1 -s
./check-service.sh &

docker-machine ssh manager docker service update --update-parallelism 1 --update-delay 5s --image=alwynpan/comp90024:demo1 nginx

echo ""
echo ""
echo "\033[0;31mdocker-machine ssh manager docker service ps nginx\033[0m"

docker-machine ssh manager docker service ps nginx

echo ""
echo ""
echo "Press [Enter] key to \033[0;34mrollback\033[0m ..."; read -k1 -s

echo ""
echo ""
echo "\033[0;31mdocker-machine ssh manager docker service update \033[0;34m--rollback\033[0m \033[0;31mnginx\033[0m"

echo ""
echo ""
echo "Press [Enter] key to \033[0;34mrollback\033[0m ..."; read -k1 -s

docker-machine ssh manager docker service update --rollback nginx

echo ""
echo ""
echo "\033[0;31mdocker-machine ssh manager docker service ps nginx\033[0m"

docker-machine ssh manager docker service ps nginx
