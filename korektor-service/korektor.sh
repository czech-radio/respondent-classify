#!/bin/bash
port=$1;
./korektor_server "$port" model cz data/korektor_model/spellchecking_h2mor_2edits.conf data/korektor_model/README
