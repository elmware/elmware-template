FROM python:3.6-slim
RUN apt-get update
RUN apt-get install -y python3-tk
WORKDIR /app
COPY ./app/requirements.txt /app
RUN pip install -r requirements.txt
COPY ./app /app
RUN chmod +x starter.sh
