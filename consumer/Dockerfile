FROM python:3.9

RUN pip install ddtrace

ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD main.py ./

ENTRYPOINT ["ddtrace-run", "python", "main.py"]
