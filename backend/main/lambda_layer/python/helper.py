from math import log
from re import sub
import uuid
import boto3
from botocore.exceptions import ClientError
import logging
from decimal import Decimal
from constants import *
from data_retrieval_settings import DataRetrievalSettings


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Helper:
    def __init__(self) -> None:
        self.textract_client = boto3.client("textract")
        self.data_retreval_settings = DataRetrievalSettings()

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
            response = table.get_item(Key={"bus_id": bus_id})
            return response["Item"]
        except ClientError as e:
            logger.error(e.response["Error"]["Message"])
            return None
