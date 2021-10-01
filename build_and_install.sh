#!/bin/bash

pip uninstall -y carebt && ./build.sh && pip install dist/carebt*.whl
