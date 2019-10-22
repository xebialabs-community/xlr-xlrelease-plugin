#!/bin/bash

set -e

./gradlew clean assemble
export plugin_jar=$(ls build/libs | sort -n | head -1)
docker-compose -f src/test/resources/docker/docker-compose.yml up -d
docker wait credentials_updater
docker logs xlr
./gradlew itest -PCHROME_HEADLESS_MODE=true
docker-compose -f src/test/resources/docker/docker-compose.yml stop
