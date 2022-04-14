#!/bin/bash

coverage run --branch --source=carebt -m pytest --cache-clear --ignore=docs --flake8 -s -vv && coverage html
