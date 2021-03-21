import logging
import os
import time

import boto3
from ddtrace import tracer
import requests


client = boto3.client("sqs")


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
