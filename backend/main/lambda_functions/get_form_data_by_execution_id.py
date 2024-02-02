import json
from logging import config
import os
import time
from constants import *
from helper import Helper
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Event: {event}")

    if event["queryStringParameters"] and "bus_id" in event["queryStringParameters"]:
        helper = Helper()
        bus_id = event["queryStringParameters"]["bus_id"]
        logger.info(f"BusId: {bus_id}")
        geo_location = helper.get_location_details_by_bus_id(bus_id)
        if geo_location:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                },
                "body": json.dumps(geo_location),
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
                "body": '{"Error": "GeoLocation is missing"}',
            }
