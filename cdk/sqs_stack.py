from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_sqs as sqs
from aws_cdk import Duration


class SqsStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, sqs_properties: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        sqs properties JSON Structure:
        {
            "queue_name": "QueueName",
            "visibility_timeout": "VisibilityTimeout",
            "retention_period": "RetentionPeriod",
            "receive_message_wait_time": "ReceiveMessageWaitTime",
            "fifo": "Fifo",
            "content_based_deduplication": "ContentBasedDeduplication"
        }
        """

        print(f"mro order x: {SqsStack.__mro__}")
        print(f"mro order y: {[cls.__name__ for cls in SqsStack.__mro__]}")

        self.sqs_properties = sqs_properties
        self.queue_name = self.sqs_properties["queue_name"]
        self.visibility_timeout = Duration.seconds(
            self.sqs_properties.get("visibility_timeout", 0)
        )
        self.retention_period = Duration.seconds(
            self.sqs_properties.get("retention_period", 345600)
        )
        self.receive_message_wait_time = Duration.seconds(
            self.sqs_properties.get("receive_message_wait_time", 0)
        )
        self.fifo = self.sqs_properties.get("fifo", False)
        self.content_based_deduplication = self.sqs_properties.get(
            "content_based_deduplication", False
        )

        self.sqs_queue = self.create_sqs_queue(
            self.queue_name,
            self.visibility_timeout,
            self.retention_period,
            self.receive_message_wait_time,
            self.fifo,
        )

    def create_sqs_queue(
        self,
        queue_name: str,
        visibility_timeout: Duration,
        retention_period: Duration,
        receive_message_wait_time: Duration,
        fifo: bool,
    ):
        fifo_throughput_limit = None
        if fifo:
            fifo_throughput_limit = (
                sqs.FifoThroughputLimit.PER_MESSAGE_GROUP_ID
                if self.content_based_deduplication
                else None
            )

        return sqs.Queue(
            self,
            queue_name,
            queue_name=queue_name,
        )

    @property
    def get_sqs_queue(self):
        return self.sqs_queue

    @property
    def get_sqs_queue_arn(self):
        return self.sqs_queue.queue_arn

    @property
    def get_sqs_queue_name(self):
        return self.sqs_queue.queue_name
