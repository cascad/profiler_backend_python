FROM python:slim

RUN mkdir /app

COPY $PWD/* /app/

RUN apt-get update && apt-get -y install build-essential

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "/app/app.py"]
