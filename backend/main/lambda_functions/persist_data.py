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
        bus_id = body.get("bus_id", None)
        geo_location_sync_id = helper.generate_unique_id()
        if bus_id:
            geo_location = body.get("geo_location", None)
            data = {
                "bus_id": bus_id,
                "geo_location": geo_location,
                "sync_id": geo_location_sync_id,
            }

            if geo_location:
                helper.save_geo_location_to_ddb(**data)
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*",
                    },
                    "body": '{"GeoLocation Saved - SyncId": "%s"}'
                    % geo_location_sync_id,
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
        else:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                },
                "body": '{"Error": "Bus Id is missing"}',
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
            "body": '{"Error": "Invalid Request"}',
        }
