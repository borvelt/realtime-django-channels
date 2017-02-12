#!/bin/bash
source /var/opt/.env/bin/activate
cd /var/opt/chatApp/
nohup daphne chatApp.asgi:channel_layer -p 8000 -b localhost -v2 &
nohup ./manage.py runworker -v2 &
