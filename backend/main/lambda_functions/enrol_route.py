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
        created_at = int(time.time())

        body["route_id"] = route_id
        body["created_at"] = created_at

        helper.save_route_to_ddb(**body)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
            },
            "body": '{"Route Saved - RouteId": "%s"}' % route_id,
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
