import logging
import os
import time

import boto3
import requests
import scrapy
from ddtrace import tracer


class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        send_to_queue(response.url.split("/")[-2])
