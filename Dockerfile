FROM mysql:8.0-debian

EXPOSE 5000 3306
WORKDIR /usr/app

ENV MYSQL_ROOT_PASSWORD=devops
ENV MYSQL_DATABASE=devops

RUN apt update -y
RUN apt install python3 python3-pip -y

COPY requirements.txt /usr/app/
RUN pip install Cmake setuptools wheel
RUN pip install --only-binary :all: greenlet
RUN pip install -r requirements.txt
RUN pip install waitress

COPY /app /usr/app/
COPY /db_dump /docker-entrypoint-initdb.d
CMD waitress-serve --host 0.0.0.0 --port 8000 app:app
