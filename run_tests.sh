#!/bin/bash

coverage run --branch --source=carebt -m pytest --cache-clear --ignore=docs -s -vv && coverage html
