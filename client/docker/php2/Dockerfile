FROM php:8.2-apache-bullseye
WORKDIR /app3
RUN apt-get update -y 
RUN apt-get install -y curl unzip gnupg xvfb libxi6 libgconf-2-4 default-jdk wget software-properties-common
RUN apt-get install -y python3-pip python3-dev build-essential libcurl4-openssl-dev libssl-dev git gcc
RUN apt-get install -y net-tools procps vim
COPY flags/readflag.c /app3/readflag.c
RUN gcc -o /readflag /app3/readflag.c
RUN chmod 111 /readflag

RUN groupadd -g 999 user
RUN useradd -r -u 999 -g user user
USER user

ENTRYPOINT /app3/entrypoint.sh && /bin/bash
CMD ["true"]
