from re import T

from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets

from backend.main.lambda_layer.python.constants import *


class Config:
    def __init__(self) -> None:

        self.__save_incoming_geo_location_lambda_properties = {
            "lambda_function": {
                "function_name": SAVE_INCOMING_GEO_LOCATION_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "persist_data.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to save incoming geo location",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_geo_location_lambda_properties = {
            "lambda_function": {
                "function_name": GET_GEO_LOCATION_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_form_data_by_execution_id.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get textract form data",
                "enable_put_metric_data": "True",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__enrol_driver_lambda_properties = {
            "lambda_function": {
                "function_name": ENROL_DRIVER_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "enrol_driver.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to enrol driver",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__geo_location_ddb_properties = {
            "name": GEO_LOCATION_TABLE,
            "partition_key": GEO_LOCATION_TABLE_PARTITION_KEY,
        }

        self.__save_geo_location_apigw_properties = {
            "rest_api_name": SAVE_GEO_LOCATION_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": SAVE_GEO_LOCATION_API_GATEWAY_PATH,
            "method": "POST",
        }

        self.__get_geo_location_apigw_properties = {
            "rest_api_name": GET_GEO_LOCATION_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_GEO_LOCATION_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__enrol_driver_ddb_properties = {
            "name": DRIVER_MASTER_TABLE,
            "partition_key": DRIVER_MASTER_TABLE_PARTITION_KEY,
        }

        self.__enrol_driver_apigw_properties = {
            "rest_api_name": ENROL_DRIVER_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": ENROL_DRIVER_API_GATEWAY_PATH,
            "method": "POST",
        }

    def get_config(self, property_name: str) -> dict:
        try:
            return getattr(self, f"_{self.__class__.__name__}__{property_name}")
        except AttributeError:
            raise ValueError(f"Config {property_name} not found")
