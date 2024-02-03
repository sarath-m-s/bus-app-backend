from math import log
from re import sub
import uuid
import boto3
from botocore.exceptions import ClientError
import logging
from constants import *
from boto3.dynamodb.conditions import Key


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
