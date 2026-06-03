FROM python:3.11-alpine
WORKDIR /app4
RUN apk add --no-cache bash \
    && pip install --no-cache-dir flask

COPY flags/command_injection_flag.txt /command_injection_flag.txt
RUN chmod 444 /command_injection_flag.txt

RUN addgroup -g 1000 user && adduser -D -u 1000 -G user user
USER user

ENTRYPOINT /app4/entrypoint.sh && /bin/sh
CMD ["true"]
