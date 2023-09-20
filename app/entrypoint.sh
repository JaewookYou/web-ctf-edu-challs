#!/bin/bash
python3 /app/app.py&
python3 /app/bot/bot.py&
python3 /app/challenges/xss1/xss1.py&
python3 /app/challenges/xss2/xss2.py&
python3 /app/challenges/xss3/xss3.py&
python3 /app/challenges/csrf1/csrf1.py&
python3 /app/challenges/csrf2/csrf2.py&
python3 /app/challenges/xsleak/xsleak.py&