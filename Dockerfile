FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 --no-cache-dir install -r requirements.txt
COPY . /app
EXPOSE 5000:80
CMD [ "python3", "app.py" ]