# Simple Website Checker
[![<romulorosa>](https://circleci.com/gh/romulorosa/simple-webchecker.svg?style=svg)](https://app.circleci.com/pipelines/github/romulorosa/simple-webchecker?branch=master)


## About

This project is intended to be a very simple website checker which periodically checks a given website status and records this information in a persistent way for further analysis.


### Components

Basically it is composed by two major components, a **checker** which is responsible for firing requests to the website, collects its data and push it to a Kafka topic. Additionally the checker can perform some sort of filtering using regex expressions which will be matched against the website content. 

The second one is the **writer**, which lies on the other side of the process and consumes messages from the topic and save all collected information into a Postgres database.


## Setup

### Requirements
Before running both checker and writer, make sure you have a Postgres database properly setup and a Kafka cluster running as well.

### Settings
The next step would be filling out your database and kafka configuration within the file **settings.py** `(webchecker/settings.py)` which can also be done using environment variables. 

Checkout both **DATABASE_CONF** and **KAFKA_CONF** located at **settings.py** to have a better picture about each information needed.

```python
DATABASE = DATABASE_CONF(
    config('DB_HOST', default=''),
    config('DB_PORT', default=''),
    config('DB_DATABASE_NAME', default=''),
    config('DB_USER', default=''),
    config('DB_PASSWORD', default=''),
)

KAFKA = KAKFA_CONF(
    config('KAFKA_BOOTSTRAPSERVER', default=''),
    config('KAFKA_TOPIC', default=''),
    config('KAFKA_CERT_FILE_PATH', default=''),
    config('KAFKA_CA_CERT_PATH', default=''),
    config('KAFKA_CERT_KEY_PATH', default=''),
)
```

### Database schema migration
Once you are ready with your database and configuration the database schema can be created making usage of CLI command just as follows.
```bash
python manage.py setupdb
```

## Running
Now that we have everything setup it is time to bring up the writer and checker. To do this, once more, the CLI option will be used. Check it below.

#### Writer
```bash
python manage.py writer
```
This command will spin up a process with a Kafka consumer which is also responsible for persisting the information inside the database.

#### Checker
The checker contains some extra options which can be really helpful for tweak a bit the default parameters. Check the options available below. 
```bash
$ python manage.py checker -h
usage: manage.py checker [-h] [-s SITES] [-i INTERVAL] [-r REGEX]

optional arguments:
  -h, --help   show this help message and exit
  -s SITES     Websites address to be monitored
  -i INTERVAL  Interval which the websites should be checked
  -r REGEX     Regex pattern to be matched against the website content

```
Please note that the `-s` option can be used multiple time in order to specify more the one website to be checked.

> **Example**
```bash
python manage.py checker -s https://www.york.ac.uk/teaching/cws/wws/webpage2.html -s https://www.york.ac.uk/teaching/cws/wws/webpage1.html -i 5
```

## Improvements
As already mentioned this is a simple website checker which has plenty room for improvements, specially in terms of performance. 

For instance, one good addition would be make usage of `async.io` in order to fetch multiple websites quickly, specially if the number of websites to be monitored is big enough to take more time than the time interval specified.

A second one which can also be chained with the previous one would be setting up celery for dispatch async tasks which will be responsible to fetch the websites. This will help on making sure that we have one task been triggered without exceeding the time aimed time interval.

The tests can also be improved, specially integration tests which tests the whole features end to end.

Furthermore, it would be nice to write some docker-compose which definitly would help newcomers to this project.


## Attributions

During the course of developing this software some references was checked for having insights and also some code snippets. The most relevant ones are listed below ;)

* https://www.tutorialspoint.com/python_data_access/
* https://gist.github.com/gruzovator/b8bc3a208f6d3dc9b275f41826285207
