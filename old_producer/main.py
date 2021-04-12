import logging
import os
import time

import boto3
from ddtrace import tracer
import requests


client = boto3.client("sqs")


@tracer.wrap("producer.send")
def send_to_queue():
    resp = client.send_message(
        QueueUrl=os.environ.get("QUEUE_URL"),
        MessageBody="test message",
    )


def main():
    logging.getLogger().setLevel(logging.INFO)
    while True:
        send_to_queue()
        logging.info("Sleeping...")
        time.sleep(30)


if __name__ == "__main__":
    main()
