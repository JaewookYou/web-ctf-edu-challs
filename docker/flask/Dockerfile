FROM python:3.11-slim-bookworm
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        chromium \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask pymysql requests selenium

ENV admin_password="[redacted]"

ENV xss1_flag="flag{[REDACTED]}"
ENV xss2_flag="flag{[REDACTED]}"
ENV xss3_flag="flag{[REDACTED]}"
ENV csrf1_flag="flag{[REDACTED]}"
ENV csrf2_flag="flag{[REDACTED]}"
ENV xsleak_flag="flag{[REDACTED]}"


ENTRYPOINT /app/entrypoint.sh && /bin/sh
CMD ["true"]
