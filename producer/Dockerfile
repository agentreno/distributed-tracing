FROM python:3.9

RUN pip install ddtrace

RUN mkdir -p /srv/app

ADD requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /srv/app
ADD . /srv/app

ENTRYPOINT ["ddtrace-run", "scrapy", "crawl", "main"]
