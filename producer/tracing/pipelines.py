import boto3
from ddtrace import tracer


@tracer.wrap("producer.send")
def send_to_queue(content):
    client = boto3.client("sqs")
    resp = client.send_message(
        QueueUrl=os.environ.get("QUEUE_URL"),
        MessageBody=content,
    )


class MainPipeline:
    def process_item(self, item, spider):
        send_to_queue(item.content)
        return item
