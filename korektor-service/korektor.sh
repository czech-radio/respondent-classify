#!/bin/bash


if [ "$#" -ne 1 ]; then
    printf 'Command should be entered in form ./korektor.sh <port>\n' >&2
    exit 1
fi


port=$1;
./korektor_server "$port" model cz data/korektor_model/spellchecking_h2mor_2edits.conf data/korektor_model/README
