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
        and "association_id" in event["queryStringParameters"]
    ):
        helper = Helper()
        association_id = event["queryStringParameters"]["association_id"]
        logger.info(f"AssociationId: {association_id}")
        association = helper.get_driver_bus_route_association_by_association_id(
            association_id
        )
        if association:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                },
                "body": json.dumps(association, cls=DecimalEncoder),
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
                "body": '{"Error": "Association is missing"}',
            }
