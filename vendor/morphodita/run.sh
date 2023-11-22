#!/bin/bash


if [ "$#" -ne 1 ]; then
    printf 'Command should be entered in form %s <port>\n' "$0"  >&2
    exit 1
fi

port=$1;
./morphodita_server "$port" model data/morphodita_model/czech-morfflex2.0-220710.dict README.md
