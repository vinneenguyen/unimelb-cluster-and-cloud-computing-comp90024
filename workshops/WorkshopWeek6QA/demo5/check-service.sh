#!/usr/bin/env bash

rm output.txt

END=15
x=$END

while [ $x -gt 0 ];
do
    echo "Run #$(($END-$x+1))" >> output.txt
    echo "" >> output.txt
    echo "" >> output.txt
    docker-machine ssh manager docker service ps nginx >> output.txt
    echo "Pause 5s ..." >> output.txt
    echo "" >> output.txt
    echo "" >> output.txt
    x=$(($x-1))
    sleep 5s
done
