#!/bin/bash
# Author: David Martin
# Proxy asset service behind a production WSGI server

cd /opt/gqlapi_service
python gqlapi/svc_cherrypy.py
