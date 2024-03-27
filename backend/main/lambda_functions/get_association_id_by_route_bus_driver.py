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

    if (
        event["queryStringParameters"]
        and "route_id" in event["queryStringParameters"]
    ):
        helper = Helper()
        route_id = event["queryStringParameters"]["route_id"]
        association_id = helper.get_association_id_by_route_id(route_id)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "association_id": association_id,
                },
                cls=DecimalEncoder,
            ),
        }
    elif (
        event["queryStringParameters"]
        and "bus_id" in event["queryStringParameters"]
    ):
        helper = Helper()
        bus_id = event["queryStringParameters"]["bus_id"]
        association_id = helper.get_association_id_by_bus_id(bus_id)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "association_id": association_id,
                },
                cls=DecimalEncoder,
            ),
        }
    elif (
        event["queryStringParameters"]
        and "driver_id" in event["queryStringParameters"]
    ):
        helper = Helper()
        driver_id = event["queryStringParameters"]["driver_id"]
        association_id = helper.get_association_id_by_driver_id(driver_id)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "association_id": association_id,
                },
                cls=DecimalEncoder,
            ),
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Invalid request",
                },
                cls=DecimalEncoder,
            ),
        }

        