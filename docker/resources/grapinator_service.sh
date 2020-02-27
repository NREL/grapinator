#!/bin/bash
# Author: David Martin
# Proxy asset service behind a production WSGI server

cd /opt/grapinator
python grapinator/svc_cherrypy.py
