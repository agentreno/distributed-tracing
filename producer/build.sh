#!/bin/bash

pipenv install
pipenv run pip freeze > requirements.txt
docker build -t karlhopkinsonturrell/distributed-tracing-producer .
docker push karlhopkinsonturrell/distributed-tracing-producer
