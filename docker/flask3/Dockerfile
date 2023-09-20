FROM ubuntu:20.04
WORKDIR /app5
RUN apt-get update -y 
RUN apt-get install -y curl unzip gnupg xvfb libxi6 libgconf-2-4 default-jdk wget software-properties-common
RUN apt-get install -y python3-pip python3-dev build-essential libcurl4-openssl-dev libssl-dev
RUN apt-get install -y net-tools vim procps
RUN pip3 install pycurl flask requests

COPY flags/ssti_flag.txt /ssti_flag.txt
RUN chmod 444 /ssti_flag.txt

RUN groupadd -g 999 user
RUN useradd -r -u 999 -g user user
USER user
RUN python3 /app5/app.py&

ENTRYPOINT /app5/entrypoint.sh && /bin/bash
CMD ["true"]
