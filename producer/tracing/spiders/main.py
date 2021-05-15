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
        ]
        with tracer.start_span("producer.start_requests") as span:
            for url in urls:
                yield scrapy.Request(
                    url=url, callback=self.parse, cb_kwargs={"span": span}
                )

    def parse(self, response, span):
        with tracer.start_span("producer.parse", child_of=span):
            return {"content": "test", "span": span}
