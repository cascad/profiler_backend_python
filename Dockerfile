FROM python:3.6-slim

RUN apt-get update && apt-get -y install build-essential git

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/profiler_frontend

COPY $PWD/ /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "/app/app.py"]
