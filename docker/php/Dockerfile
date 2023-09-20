FROM php:8.2-apache-bullseye
WORKDIR /app2
RUN apt-get update -y 
RUN apt-get install -y curl unzip gnupg xvfb libxi6 libgconf-2-4 default-jdk wget software-properties-common
RUN apt-get install -y python3-pip python3-dev build-essential libcurl4-openssl-dev libssl-dev git
RUN apt-get install -y net-tools
RUN apt-get install -y procps
RUN docker-php-ext-install mysqli

COPY flags/domclobbering_flag.txt /domclobbering_flag.txt
RUN chmod 444 /domclobbering_flag.txt

COPY flags/sqli1_flag.txt /sqli1_flag.txt
RUN chmod 444 /sqli1_flag.txt

COPY flags/sqli2_flag.txt /sqli2_flag.txt
RUN chmod 444 /sqli2_flag.txt

COPY flags/pp_flag.txt /pp_flag.txt
RUN chmod 444 /pp_flag.txt

RUN groupadd -g 999 user
RUN useradd -r -u 999 -g user user
USER user

ENTRYPOINT /app2/entrypoint.sh && /bin/bash
CMD ["true"]
