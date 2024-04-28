#!/bin/sh
set -e  # Configure shell so that if one command fails, it exits
coverage erase
coverage run tests/runtests.py
coverage report
coverage html
