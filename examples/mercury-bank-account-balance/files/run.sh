#!/bin/bash
rngd -v
/gvisor-tap-vsock-main/bin/vm -debug &> /dev/null &
sleep 10
mkdir -p /run/resolvconf
echo "nameserver 192.168.127.1" > /run/resolvconf/resolv.conf
service ssh start
python3 main.py
