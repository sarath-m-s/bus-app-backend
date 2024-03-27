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

        self.__get_driver_details_lambda_properties = {
            "lambda_function": {
                "function_name": GET_DRIVER_DETAILS_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_driver_details.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get driver details",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__enrol_bus_lambda_properties = {
            "lambda_function": {
                "function_name": ENROL_BUS_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "enrol_bus.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to enrol bus",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_bus_details_lambda_properties = {
            "lambda_function": {
                "function_name": GET_BUS_DETAILS_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_bus_details.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get bus details",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__enrol_route_lambda_properties = {
            "lambda_function": {
                "function_name": ENROL_ROUTE_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "enrol_route.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to enrol route",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_route_details_lambda_properties = {
            "lambda_function": {
                "function_name": GET_ROUTE_DETAILS_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_route_details.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get route details",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__associate_driver_bus_route_lambda_properties = {
            "lambda_function": {
                "function_name": ASSOCIATE_DRIVER_BUS_ROUTE_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "associate_driver_bus_route.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to associate driver, bus and route",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_driver_bus_route_association_lambda_properties = {
            "lambda_function": {
                "function_name": GET_DRIVER_BUS_ROUTE_ASSOCIATION_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_driver_bus_route_association.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get driver, bus and route association",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_association_id_by_route_bus_driver_lambda_properties = {
            "lambda_function": {
                "function_name": GET_ASSOCIATION_ID_BY_BUS_ROUTE_DRIVER_ID_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_association_id_by_route_bus_driver.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get association id by route, bus and driver",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_all_driver_details_lambda_properties = {
            "lambda_function": {
                "function_name": GET_ALL_DRIVER_DETAILS,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_all_driver_details.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get all driver details",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_all_bus_details_lambda_properties = {
            "lambda_function": {
                "function_name": GET_ALL_BUS_DETAILS,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_all_bus_details.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get all bus details",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__get_all_route_details_lambda_properties = {
            "lambda_function": {
                "function_name": GET_ALL_ROUTE_DETAILS,
                "asset_path": "backend/main/lambda_functions",
                "handler": "get_all_route_details.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get all route details",
                "enable_put_metric_data": "False",
            },
            "lambda_layer": {
                "asset_path": "backend/main/lambda_layer",
                "layer_name": f"{APPLICATION_NAME}_lambda_layer",
                "description": f"{APPLICATION_NAME} Layer",
            },
            "event_source_mapping_properties": {},
        }

        self.__google_maps_wrapper_lambda_properties = {
            "lambda_function": {
                "function_name": GOOGLE_MAPS_WRAPPER_LAMBDA,
                "asset_path": "backend/main/lambda_functions",
                "handler": "google_maps_wrapper.handler",
                "runtime": "python3.8",
                "timeout": 300,
                "memory_size": 128,
                "description": "Lambda function to get google maps data",
                "enable_put_metric_data": "True",
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

        self.__get_driver_details_apigw_properties = {
            "rest_api_name": GET_DRIVER_DETAILS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_DRIVER_DETAILS_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__enrol_bus_ddb_properties = {
            "name": BUS_MASTER_TABLE,
            "partition_key": BUS_MASTER_TABLE_PARTITION_KEY,
        }

        self.__enrol_bus_apigw_properties = {
            "rest_api_name": ENROL_BUS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": ENROL_BUS_API_GATEWAY_PATH,
            "method": "POST",
        }

        self.__get_bus_details_apigw_properties = {
            "rest_api_name": GET_BUS_DETAILS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_BUS_DETAILS_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__google_maps_wrapper_apigw_properties = {
            "rest_api_name": GOOGLE_MAPS_WRAPPER_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GOOGLE_MAPS_WRAPPER_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__enrol_route_ddb_properties = {
            "name": ROUTE_MASTER_TABLE,
            "partition_key": ROUTE_MASTER_TABLE_PARTITION_KEY,
        }

        self.__enrol_route_apigw_properties = {
            "rest_api_name": ENROL_ROUTE_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": ENROL_ROUTE_API_GATEWAY_PATH,
            "method": "POST",
        }

        self.__get_route_details_apigw_properties = {
            "rest_api_name": GET_ROUTE_DETAILS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_ROUTE_DETAILS_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__associate_driver_bus_route_ddb_properties = {
            "name": ASSOCIATION_TABLE,
            "partition_key": ASSOCIATION_TABLE_PARTITION_KEY,
        }

        self.__associate_driver_bus_route_apigw_properties = {
            "rest_api_name": ASSOCIATE_DRIVER_BUS_ROUTE_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": ASSOCIATE_DRIVER_BUS_ROUTE_API_GATEWAY_PATH,
            "method": "POST",
        }

        self.__get_driver_bus_route_association_apigw_properties = {
            "rest_api_name": GET_DRIVER_BUS_ROUTE_ASSOCIATION_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_DRIVER_BUS_ROUTE_ASSOCIATION_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__get_assciation_id_by_route_bus_driver_apigw_properties = {
            "rest_api_name": GET_ASSOCIATION_ID_BY_ROUTE_BUS_DRIVER_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_ASSOCIATION_ID_BY_ROUTE_BUS_DRIVER_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__get_all_driver_details_apigw_properties = {
            "rest_api_name": GET_ALL_DRIVER_DETAILS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_ALL_DRIVER_DETAILS_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__get_all_bus_details_apigw_properties = {
            "rest_api_name": GET_ALL_BUS_DETAILS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_ALL_BUS_DETAILS_API_GATEWAY_PATH,
            "method": "GET",
        }

        self.__get_all_route_details_apigw_properties = {
            "rest_api_name": GET_ALL_ROUTE_DETAILS_API_GATEWAY_NAME,
            "api_key_required": False,
            "timeout": 10,
            "integration": {
                "type": "lambda",
            },
            "part_path": GET_ALL_ROUTE_DETAILS_API_GATEWAY_PATH,
            "method": "GET",
        }

    def get_config(self, property_name: str) -> dict:
        try:
            return getattr(self, f"_{self.__class__.__name__}__{property_name}")
        except AttributeError:
            raise ValueError(f"Config {property_name} not found")
