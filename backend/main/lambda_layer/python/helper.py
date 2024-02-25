import logging
import uuid
from math import log
from re import sub

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from constants import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Helper:
    def __init__(self) -> None:
        self.textract_client = boto3.client("textract")

    def generate_unique_id(self):
        return str(uuid.uuid4())

    def save_geo_location_to_ddb(self, **kwargs):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(GEO_LOCATION_TABLE)
        response = table.put_item(
            Item={
                "bus_id": kwargs["bus_id"],
                "geo_location": kwargs["geo_location"],
                "sync_id": kwargs["sync_id"],
            }
        )

    def get_location_details_by_bus_id(self, bus_id):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(GEO_LOCATION_TABLE)
        try:
            response = table.query(KeyConditionExpression=Key("bus_id").eq(bus_id))
            return response["Items"]
        except ClientError as e:
            logger.error(e.response["Error"]["Message"])
            return None

    def save_bus_to_ddb(self, **kwargs):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(BUS_TABLE)
        response = table.put_item(
            Item={
                "bus_id": kwargs["bus_id"],
                "bus_name": kwargs["bus_name"],
                "registration_number": kwargs["registration_number"],
                "bus_type": kwargs["bus_type"],
            }
        )

    def get_bus_details_by_busid(self, bus_id):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(BUS_MASTER_TABLE)
        try:
            response = table.query(KeyConditionExpression=Key("bus_id").eq(bus_id))
            return response["Items"]
        except ClientError as e:
            logger.error(e.response["Error"]["Message"])
            return None

    def save_driver_to_ddb(self, **kwargs):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(DRIVER_MASTER_TABLE)
        response = table.put_item(
            Item={
                "driver_id": kwargs["driver_id"],
                "driver_name": kwargs["driver_name"],
                "contact_number": kwargs["contact_number"],
                "license_number": kwargs.get("license_number", "Not Provided"),
                "organization": kwargs.get("organization", "Not Provided"),
                "address": kwargs.get("address", "Not Provided"),
                "created_at": kwargs["created_at"],
            }
        )
