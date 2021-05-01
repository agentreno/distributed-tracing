#!/bin/bash

docker build -t karlhopkinsonturrell/distributed-tracing-api:${1:latest} .
docker push karlhopkinsonturrell/distributed-tracing-api:${1:latest}
