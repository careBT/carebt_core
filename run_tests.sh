#!/bin/bash

coverage run --source=carebt -m pytest --cache-clear --flake8 -s && coverage html
