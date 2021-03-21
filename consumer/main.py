import logging
import os
import time

from ddtrace import tracer
import requests


@tracer.wrap("queue.poll")
def poll_queue():
    requests.get("https://google.com")


def main():
    logging.getLogger().setLevel(logging.INFO)
    while True:
        poll_queue()
        logging.info("Sleeping...")
        time.sleep(5)


if __name__ == "__main__":
    main()
