import logging
import os
import time

import boto3
from ddtrace import tracer
import requests


class ReceivedMessageFilter:
    def process_trace(self, trace):
        if any(span.resource == "sqs.deletemessage" for span in trace):
            return trace

        return None


class LoggingFilter:
    def process_trace(self, trace):
        for span in trace:
            logging.info(span.name)
            logging.info(span.service)
            logging.info(span.resource)

        return trace


client = boto3.client("sqs")
tracer.configure(settings={
    "FILTERS": [ReceivedMessageFilter()]
})


@tracer.wrap("queue.poll")
def poll_queue():
    resp = client.receive_message(QueueUrl=os.environ.get("QUEUE_URL"))

    if "Messages" in resp:
        for message in resp["Messages"]:
            logging.info("Received message")
            logging.info(message)
            client.delete_message(
                QueueUrl=os.environ.get("QUEUE_URL"),
                ReceiptHandle=message["ReceiptHandle"],
            )


def main():
    logging.getLogger().setLevel(logging.INFO)
    while True:
        poll_queue()
        logging.info("Sleeping...")
        time.sleep(5)


if __name__ == "__main__":
    main()
