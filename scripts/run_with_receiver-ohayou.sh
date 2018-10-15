#!/bin/bash

cd $(dirname $0)

echo 'starting julius server.'
PID=$(./julius-start-ohayou.sh)

python3 ../src/python/receiver.py

trap - INT
kill $PID

exit 0
