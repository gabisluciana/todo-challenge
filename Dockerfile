FROM python:3.10.13-alpine3.19

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN pip install --upgrade pip 

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt --no-cache-dir 

COPY . /app/

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]