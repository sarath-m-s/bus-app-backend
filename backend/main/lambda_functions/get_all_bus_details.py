import json
import logging
import os
import time

from constants import *
from helper import Helper
from json_encoder import DecimalEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Event: {event}")

    helper = Helper()
    bus_details = helper.get_all_bus_details()

    if bus_details:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
            },
            "body": json.dumps(bus_details, cls=DecimalEncoder),
        }
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
            },
            "body": '{"Error": "Bus details are missing"}',
        }
