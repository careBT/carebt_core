#!/bin/bash

coverage run --source=carebt -m pytest --cache-clear --flake8 && coverage html
