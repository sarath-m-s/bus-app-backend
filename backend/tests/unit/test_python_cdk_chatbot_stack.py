import unittest
from aws_cdk_lib import core
from python_cdk_chatbot.python_cdk_chatbot_stack import PythonCdkChatbotStack
from main.lambda_layer.python.constants import PUT_INCOMING_CHAT_MESSAGE_TO_SQS_LAMBDA


class TestQueueCreation(unittest.TestCase):
    def setUp(self):
        self.app = core.App()
        self.stack = PythonCdkChatbotStack(self.app, "TestStack")

    def test_queue_creation(self):
        # Retrieve the queue from the stack
        queue = self.stack.node.find_child(PUT_INCOMING_CHAT_MESSAGE_TO_SQS_LAMBDA)

        # Assert that the queue exists
        self.assertIsNotNone(queue)


if __name__ == "__main__":
    unittest.main()
