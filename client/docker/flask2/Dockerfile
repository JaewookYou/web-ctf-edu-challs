FROM ubuntu:20.04
WORKDIR /app4
RUN apt-get update -y 
RUN apt-get install -y curl unzip gnupg xvfb libxi6 libgconf-2-4 default-jdk wget software-properties-common
RUN apt-get install -y python3-pip python3-dev build-essential libcurl4-openssl-dev libssl-dev
RUN apt-get install -y net-tools vim procps
RUN pip3 install pycurl flask requests

COPY flags/command_injection_flag.txt /command_injection_flag.txt
RUN chmod 444 /command_injection_flag.txt

ENTRYPOINT /app4/entrypoint.sh && /bin/bash
CMD ["true"]
