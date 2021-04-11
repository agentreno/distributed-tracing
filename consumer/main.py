import json
import logging
import os
import time

import boto3
from ddtrace import tracer, context
from prometheus_client import start_http_server, Counter


QUEUE_POLL_COUNT = Counter("queue_poll_count", "SQS Queue poll counter")


class ProcessMessageFilter:
    def process_trace(self, trace):
        if any(span.name == "consumer.process_messages" for span in trace):
            return trace

        return None


class LoggingFilter:
    def process_trace(self, trace):
        for span in trace:
            logging.info(span.name)
            logging.info(span.service)
            logging.info(span.resource)

        return trace


class SQSContextExtractor:
    def process_message(self, message):
        # These attributes seem to be injected automatically by ddtrace on the
        # producer side But they're not documented and they should be (but
        # arent) being extracted automatically on the consumer side Probably
        # ongoing work similar to
        # https://github.com/DataDog/dd-trace-java/issues/1823
        if "MessageAttributes" in message and "_datadog" in message["MessageAttributes"]:
            logging.info("Found datadog trace context")
            trace_context_data = json.loads(message["MessageAttributes"]["_datadog"]["StringValue"])
            trace_id = int(trace_context_data.get("x-datadog-trace-id"))

            # The reason I'm not using parent_id from the message is because
            # processing this message is not part of the span in the producer.
            # Rather it's the next span in a sequence. So I'm not setting
            # context.span_id, we want a new span. But they're both part of the
            # same trace still.
            if trace_id:
                return context.Context(trace_id=trace_id)

        return None


client = boto3.client("sqs")
sqs_context_extractor = SQSContextExtractor()
tracer.configure(settings={
    "FILTERS": [ProcessMessageFilter()]
})


@tracer.wrap("consumer.poll")
def poll_queue():
    QUEUE_POLL_COUNT.inc()
    resp = client.receive_message(
        QueueUrl=os.environ.get("QUEUE_URL"),
        MessageAttributeNames=["All"],
    )

    if "Messages" not in resp:
        return

    for message in resp["Messages"]:
        context = sqs_context_extractor.process_message(message)
        if context:
            logging.info("Activating context")
            logging.info(context)
            tracer.context_provider.activate(context)

        with tracer.trace("consumer.process_messages"):
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
    # Prometheus metrics server
    start_http_server(8000)

    main()
