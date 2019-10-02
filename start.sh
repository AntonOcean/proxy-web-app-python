#!/bin/bash

gunicorn --workers 2 --log-level=info --name app -b 0.0.0.0:8080 main:init_app --worker-class aiohttp.GunicornWebWorker --timeout 90