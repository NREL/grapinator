#!/usr/bin/env sh
# Author: David Martin
# Proxy service behind a production WSGI server

cd /opt/grapinator
python3 grapinator/svc_cherrypy.py
