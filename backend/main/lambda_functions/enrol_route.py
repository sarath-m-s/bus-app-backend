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

        route_id = helper.generate_unique_id()
        route_name = body.get("route_name", None)
        bus_id = body.get("bus_id", None)
        start_location = body.get("start_location", None)
        end_location = body.get("end_location", None)
        start_time = body.get("start_time", None)
        end_time = body.get("end_time", None)
