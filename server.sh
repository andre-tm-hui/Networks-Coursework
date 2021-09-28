#!/bin/bash

chmod +x server.py

python3 server.py || python server.py

echo "Server Offline"$'\r' >> server.log

echo Server Offline

sleep 2
