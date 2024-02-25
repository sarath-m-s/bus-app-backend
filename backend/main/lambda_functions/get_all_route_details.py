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
    route_details = helper.get_all_route_details()

    if route_details:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
            },
            "body": json.dumps(route_details, cls=DecimalEncoder),
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
            "body": '{"Error": "Route details are missing"}',
        }
