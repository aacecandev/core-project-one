#!/bin/bash

set -xeou pipefail

echo "Creating mongo users..."
mongo admin --host localhost -u "${MONGO_INITDB_ROOT_USERNAME}" \
  -p "${MONGO_INITDB_ROOT_PASSWORD}" \
  --eval "db.createUser({user: \"${MONGO_NON_ROOT_USERNAME}\", pwd: \"${MONGO_NON_ROOT_PASSWORD}\", roles: [{role: \"${MONGO_NON_ROOT_ROLE}\", db: \"${MONGO_NON_ROOT_DB}\"}]});"
echo "Mongo users created."
