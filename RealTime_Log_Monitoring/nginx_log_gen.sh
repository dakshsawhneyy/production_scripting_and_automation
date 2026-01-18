#!/bin/bash

ips=("192.168.2.3" "192.168.5.6" "172.168.9.7" "8.8.8.8" "0.0.0.0")
images=("hello.png" "yoyo.png" "animal.png" "server.jpeg")
status_code=("500" "200" "202" "404" "300")

log_file="$(dirname "$0")/access.log"

while true; do
    ip=${ips[$((RANDOM % ${#ips[@]}))]}
    date=$(date +"%d/%m/%Y:%H:%M:%S")
    image=${images[$((RANDOM % ${#images[@]}))]}
    status=${status_code[$((RANDOM % ${#status_code[@]}))]}

    echo -e "$ip - - [$date +0000] \"GET $image HTTP/1.1\" $status" >> $log_file
done