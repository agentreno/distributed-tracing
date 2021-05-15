import boto3
import requests
import scrapy
from ddtrace import tracer, patch

patch(botocore=True)


class MainSpider(scrapy.Spider):
    name = "main"
    ITEM_PIPELINES = {
        "tracing.pipelines.MainPipeline": 300,
    }

    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/page/1/",
            "http://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            with tracer.start_span("producer.parse") as span:
                return {"content": quote.css("span.text::text").get(), "span": span}
