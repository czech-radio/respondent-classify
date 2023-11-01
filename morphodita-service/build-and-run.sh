#!/bin/bash

if [ "$#" -ne 1 ]; then
    printf 'Command should be entered in form ./build-and-run.sh <port>\n' >&2
    exit 1
fi

bash build.sh
bash morphodita.sh "$1"