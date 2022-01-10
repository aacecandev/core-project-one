#!/bin/bash
set -xeou pipefail

mongoimport --host localhost --port 27017 --username "${MONGO_NON_ROOT_USERNAME}" --password "${MONGO_NON_ROOT_PASSWORD}" --db "${MONGO_NON_ROOT_DB}" --collection accidents --authenticationDatabase admin --authenticationMechanism=SCRAM-SHA-256 --drop --file /docker-entrypoint-initdb.d/accidents_fixed.json

mongo localhost/"${MONGO_NON_ROOT_DB}" -u "${MONGO_NON_ROOT_USERNAME}" -p "${MONGO_NON_ROOT_PASSWORD}" --authenticationDatabase admin --eval 'db.accidents.updateMany({},[{"$set": {date: {"$add": [new Date("1970-01-01"),"$date"]}}}]);'
