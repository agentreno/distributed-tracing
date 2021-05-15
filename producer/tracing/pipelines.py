import os

import boto3
from ddtrace import tracer


def send_to_queue(content, span):
    tracer.context_provider.activate(span.context)
    with tracer.start_span("producer.send", child_of=span):
        client = boto3.client("sqs")
        client.send_message(
            QueueUrl=os.environ.get("QUEUE_URL"),
            MessageBody=content,
        )


class MainPipeline:
    def process_item(self, item, spider):
        send_to_queue(item["content"], item["span"])
        return item
