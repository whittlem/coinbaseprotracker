FROM python:3.9.5-slim-buster

WORKDIR /app

COPY requirements.txt /app/

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENTRYPOINT [ "python3", "-u", "coinbaseprotracker.py" ]