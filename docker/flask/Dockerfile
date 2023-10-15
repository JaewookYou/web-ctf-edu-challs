FROM ubuntu:20.04
WORKDIR /app
RUN apt-get update -y 
RUN apt-get install -y curl unzip gnupg xvfb libxi6 libgconf-2-4 default-jdk wget software-properties-common
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y && apt-get install -y google-chrome-stable
RUN apt-get install -y python3-pip python3-dev build-essential libcurl4-openssl-dev libssl-dev git
RUN apt-get install -y net-tools
RUN apt-get install -y procps
RUN pip3 install pycurl pymysql flask requests selenium
RUN pip3 install git+https://github.com/SergeyPirogov/webdriver_manager

ENV admin_password [redacted]

ENV xss1_flag flag{[redacted]}
ENV xss2_flag flag{[redacted]}
ENV xss3_flag flag{[redacted]}
ENV csrf1_flag flag{[redacted]}
ENV csrf2_flag flag{[redacted]}
ENV xsleak_flag flag{[redacted]}


ENTRYPOINT /app/entrypoint.sh && /bin/bash
CMD ["true"]
