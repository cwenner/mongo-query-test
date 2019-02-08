#!/bin/bash

set -e

docker pull mongo:3.6
docker run --rm -p 27017:27017 mongo:3.6
