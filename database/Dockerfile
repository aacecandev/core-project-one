FROM mongo:4.4

# Maintainer of the Dockerfile
LABEL maintainer="Alejandro Aceituna Cano - dev@aacecan.com"

# Environment variables
ENV TZ=Europe/Madrid

#  Set the time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy executables to ENTRYPOINT executable dir
COPY ./entrypoint.sh /docker-entrypoint-initdb.d/
COPY ./mongo-import.sh /docker-entrypoint-initdb.d/

# Copy JSON seed
COPY ./accidents_fixed.json /docker-entrypoint-initdb.d/
