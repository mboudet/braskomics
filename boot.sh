#!/bin/sh
exec gunicorn -b :81 --access-logfile - --error-logfile - braskomics:app
