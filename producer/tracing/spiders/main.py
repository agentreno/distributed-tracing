import logging
import os
import time

import boto3
import requests
import scrapy
from ddtrace import tracer


@tracer.wrap("producer.send")
def send_to_queue(content):
    client = boto3.client("sqs")
    resp = client.send_message(
        QueueUrl=os.environ.get("QUEUE_URL"),
        MessageBody=content,
    )


class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        send_to_queue(response.url.split("/")[-2])
