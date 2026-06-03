FROM php:8.2-apache-bookworm
WORKDIR /app3
COPY flags/readflag.c /app3/readflag.c
RUN gcc -o /readflag /app3/readflag.c
RUN chmod 111 /readflag

RUN groupadd -g 999 user
RUN useradd -r -u 999 -g user user
USER user

ENTRYPOINT /app3/entrypoint.sh && /bin/sh
CMD ["true"]
