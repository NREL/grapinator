#!/usr/bin/env bash
# Author: David Martin
# Proxy service behind a production WSGI server

cd /opt/grapinator
python3 grapinator/svc_cherrypy.py
