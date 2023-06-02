#!/bin/sh
pip install psycopg2==2.7.3.2 bottle==0.12.13 requests pypika==0.48.9 bottle-cors-plugin
python -u web-api.py
