FROM mongo:4.4

# Maintainer of the Dockerfile
LABEL maintainer="Alejandro Aceituna Cano - dev@aacecan.com"

# Environment variables
ENV TZ=Europe/Madrid

#  Set the time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy entrypoint.sh to ENTRYPOINT executable dir
COPY ./entrypoint.sh /docker-entrypoint-initdb.d/
