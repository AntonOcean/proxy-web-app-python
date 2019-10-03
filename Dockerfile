FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV DOCKER_DB_LINK mongo_db
RUN mkdir /proxy-app
WORKDIR /proxy-app

COPY requirements.txt /proxy-app/
RUN pip install -r requirements.txt

COPY . /proxy-app/

EXPOSE 8080
EXPOSE 9090

WORKDIR /proxy-app/src

ENTRYPOINT ["sh", "../start.sh"]