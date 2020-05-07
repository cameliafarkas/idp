# Derived from official mysql image (our base image)
FROM mysql:5.6
# Add a database

ENV MYSQL_DATABASE=$MYSQL_DATABASE
ENV MYSQL_USER=$MYSQL_USER
ENV MYSQL_PASSWORD=$MYSQL_PASSWORD
ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

WORKDIR /app


COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
