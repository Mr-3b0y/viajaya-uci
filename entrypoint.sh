#!/bin/sh

# Iniciar Gunicorn
# exec gunicorn --bind 0.0.0.0:8000 configs.wsgi:application &

# Iniciar Nginx
exec nginx -g "daemon off;"