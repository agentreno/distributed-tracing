#!/bin/bash

pipenv install
pipenv run pip freeze > requirements.txt
docker build -t karlhopkinsonturrell/distributed-tracing-consumer .
docker push karlhopkinsonturrell/distributed-tracing-consumer
