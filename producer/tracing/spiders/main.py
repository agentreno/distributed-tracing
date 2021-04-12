import boto3
import requests
import scrapy


class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = ["https://www.google.com"]
    ITEM_PIPELINES = {
        "tracing.pipelines.MainPipeline": 300,
    }

    def parse(self, response):
        return {"content": "test"}
