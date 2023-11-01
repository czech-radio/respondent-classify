#!/bin/bash

if [ "$#" -ne 1 ]; then
    printf 'Command should be entered in form %s <port>\n' "$0"  >&2
    exit 1
fi

bash build.sh
bash korektor.sh "$1"