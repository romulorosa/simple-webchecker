FROM python:3.8.2

WORKDIR /usr/src/app

COPY . ./
RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
