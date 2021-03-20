FROM python:3.9

RUN pip install pipenv ddtrace

ADD Pipfile Pipfile.lock main.py ./

RUN pipenv install

ENTRYPOINT ["pipenv", "run", "ddtrace-run", "python", "main.py"]
