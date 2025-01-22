FROM python:3.12-alpine

RUN mkdir /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY fixtures /app/fixtures
COPY main /app/main
COPY env_conf.py /app
COPY .env /app

WORKDIR /app

ENTRYPOINT ["gunicorn", "main:app", "w 2", "-b", "0.0.0.0:8000"]
