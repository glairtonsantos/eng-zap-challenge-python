#!/bin/sh
gunicorn --chdir eng_zap_challenge_python wsgi:app -b 0.0.0.0:5000