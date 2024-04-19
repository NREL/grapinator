#!/usr/bin/env sh
# Author: David Martin
# Proxy service behind a production WSGI server

cd /opt/grapinator
source venv/bin/activate
python grapinator/svc_cherrypy.py
