#!/bin/bash

coverage run --branch --source=carebt -m pytest --cache-clear --flake8 -s -vv && coverage html
