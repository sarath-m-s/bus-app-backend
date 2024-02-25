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

        driver_id = body["driver_id"]
        bus_id = body["bus_id"]
        route_id = body["route_id"]
        created_at = int(time.time())
        associattion_id = helper.generate_unique_id()

        association = {
            "association_id": associattion_id,
            "driver_id": driver_id,
            "bus_id": bus_id,
            "route_id": route_id,
            "created_at": created_at,
        }

        helper.save_association_to_ddb(**association)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
            },
            "body": '{"Association Saved - AssociationId": "%s"}' % associattion_id,
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
            "body": '{"Error": "Association details are missing"}',
        }
