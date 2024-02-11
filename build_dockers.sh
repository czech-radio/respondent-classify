#!/bin/bash
docker build -t korektor vendor/korektor
docker build -t morphodita vendor/morphodita
docker build -t labeler .
