FROM python:3.9

RUN pip install pipenv

RUN mkdir -p /srv/app
WORKDIR /srv/app

ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install

ADD . .

ENTRYPOINT ["./docker-entrypoint.sh"]
