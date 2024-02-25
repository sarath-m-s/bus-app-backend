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

    if event["queryStringParameters"] and "driver_id" in event["queryStringParameters"]:
        helper = Helper()
        driver_id = event["queryStringParameters"]["driver_id"]
        logger.info(f"DriverId: {driver_id}")
        driver = helper.get_driver_details_by_driver_id(driver_id)
        if driver:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                },
                "body": json.dumps(driver, cls=DecimalEncoder),
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
                "body": '{"Error": "Driver is missing"}',
            }
