import json
import logging
import os
import time

from constants import *
from helper import Helper

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Event: {event}")

    if ("body" in event) and event["body"]:
        helper = Helper()
        body = json.loads(event["body"])
        if "payload" in body:
            body = json.loads(body["payload"])

        logger.info(f"Body: {body}")

        new_bus_id = helper.generate_unique_id()
        bus_name = body.get("bus_name", None)
        registration_number = body.get("registration_number", None)
        bus_type = body.get("bus_type", None)

        if bus_name and registration_number and bus_type:
            data = {
                "bus_id": new_bus_id,
                "bus_name": bus_name,
                "registration_number": registration_number,
                "bus_type": bus_type,
            }

            helper.save_bus_to_ddb(**data)
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                },
                "body": '{"Bus Saved - BusId": "%s"}' % new_bus_id,
            }
