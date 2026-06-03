FROM python:3.11-alpine
WORKDIR /app5
RUN pip install --no-cache-dir flask

COPY flags/ssti_flag.txt /ssti_flag.txt
RUN chmod 444 /ssti_flag.txt

RUN addgroup -g 1000 user && adduser -D -u 1000 -G user user
USER user

ENTRYPOINT /app5/entrypoint.sh && /bin/sh
CMD ["true"]
