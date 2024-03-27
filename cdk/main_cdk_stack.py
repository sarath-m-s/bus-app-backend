from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from constructs import Construct

from backend.main.lambda_layer.python.constants import (
    CLOUDWATCH_LOGS_PERMISSIONS, CLOUDWATCH_LOGS_RESOURCES)

from .apigw_stack import ApiGatewayStack
from .config import Config
from .ddb_stack import DynamoDBStack
from .eventbridge_stack import EventBridgeStack
from .iam_stack import Iam
from .lambda_stack import DeployLambdaStack
from .s3_stack import S3Stack
from .sqs_stack import SqsStack
from .step_functions_stack import StepFunctionsStack


class BusAppAwsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.config = Config()
        self.cw_logs_permissions = CLOUDWATCH_LOGS_PERMISSIONS
        self.cw_logs_resources = CLOUDWATCH_LOGS_RESOURCES

        self.geo_location_ddb = self.create_textract_ddb_table(**kwargs)
        self.save_geo_location_lambda = self.create_save_geo_location_to_ddb_lambda(
            **kwargs
        )
        self.get_geo_location_lambda = self.create_get_geo_location_from_ddb_lambda(
            **kwargs
        )
        self.save_geo_location_api = self.create_save_geo_location_api(**kwargs)
        self.get_geo_location_api = self.create_get_geo_location_api(**kwargs)
        self.enrol_driver_ddb = self.create_enrol_driver_ddb_table(**kwargs)
        self.enrol_driver_lambda = self.create_enrol_driver_lambda(**kwargs)
        self.enrol_driver_api = self.create_enrol_driver_api(**kwargs)
        self.get_driver_details_lambda = self.create_get_driver_details_lambda(**kwargs)
        self.get_driver_details_api = self.create_get_driver_details_api(**kwargs)
        self.enrol_bus_ddb = self.create_enrol_bus_ddb_table(**kwargs)
        self.enrol_bus_lambda = self.create_enrol_bus_lambda(**kwargs)
        self.enrol_bus_api = self.create_enrol_bus_api(**kwargs)
        self.get_bus_details_lambda = self.create_get_bus_details_lambda(**kwargs)
        self.get_bus_details_api = self.create_get_bus_details_api(**kwargs)
        self.enrol_route_ddb = self.create_enrol_route_ddb_table(**kwargs)
        self.enrol_route_lambda = self.create_enrol_route_lambda(**kwargs)
        self.enrol_route_api = self.create_enrol_route_api(**kwargs)
        self.get_route_details_lambda = self.create_get_route_details_lambda(**kwargs)
        self.get_route_details_api = self.create_get_route_details_api(**kwargs)
        self.associate_driver_bus_route_ddb_table = (
            self.create_associate_driver_bus_route_ddb_table(**kwargs)
        )
        self.get_driver_bus_route_association_lambda = (
            self.create_get_driver_bus_route_association_lambda(**kwargs)
        )
        self.associate_driver_bus_route_lambda = (
            self.create_associate_driver_bus_route_lambda(**kwargs)
        )
        self.associate_driver_bus_route_api = (
            self.create_associate_driver_bus_route_api(**kwargs)
        )
        self.get_route_bus_driver_association_lambda = (
            self.create_get_route_bus_driver_association_lambda(**kwargs)
        )

        self.get_route_bus_driver_association_api = (
            self.create_get_route_bus_driver_association_api(**kwargs)
        )

        self.get_all_driver_details_lambda = self.create_get_all_driver_details_lambda(
            **kwargs
        )
        self.get_all_driver_details_api = self.create_get_all_driver_details_api(
            **kwargs
        )
        self.get_all_bus_details_lambda = self.create_get_all_bus_details_lambda(
            **kwargs
        )
        self.get_all_bus_details_api = self.create_get_all_bus_details_api(**kwargs)
        self.get_all_route_details_lambda = self.create_get_all_route_details_lambda(
            **kwargs
        )
        self.get_all_route_details_api = self.create_get_all_route_details_api(**kwargs)
        self.google_maps_lambda = self.create_google_maps_lambda(**kwargs)
        self.google_maps_api = self.create_google_maps_api(**kwargs)

    def create_textract_ddb_table(self, **kwargs):
        ddb_table = DynamoDBStack(
            self,
            "BusAppDDBTable",
            self.config.get_config("geo_location_ddb_properties"),
            **kwargs,
        )
        return ddb_table

    def create_save_geo_location_to_ddb_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "save_incoming_geo_location_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:PutItem",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.geo_location_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "SaveGeoLocationLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        save_geo_location_lambda = DeployLambdaStack(
            self,
            "SaveGeoLocationLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return save_geo_location_lambda

    def create_get_geo_location_from_ddb_lambda(self, **kwargs):
        lambda_properties = self.config.get_config("get_geo_location_lambda_properties")

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.geo_location_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetGeoLocationLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_geo_location_lambda = DeployLambdaStack(
            self,
            "GetGeoLocationLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_geo_location_lambda

    def create_save_geo_location_api(self, **kwargs):
        api_properties = self.config.get_config("save_geo_location_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.save_geo_location_lambda.lambda_function

        save_geo_location_api = ApiGatewayStack(
            self,
            "SaveGeoLocationApi",
            api_properties,
            **kwargs,
        )

        return save_geo_location_api

    def create_get_geo_location_api(self, **kwargs):
        api_properties = self.config.get_config("get_geo_location_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.get_geo_location_lambda.lambda_function

        get_geo_location_api = ApiGatewayStack(
            self,
            "GetGeoLocationApi",
            api_properties,
            **kwargs,
        )

        return get_geo_location_api

    def create_enrol_driver_ddb_table(self, **kwargs):
        ddb_table = DynamoDBStack(
            self,
            "EnrolDriverDDBTable",
            self.config.get_config("enrol_driver_ddb_properties"),
            **kwargs,
        )
        return ddb_table

    def create_enrol_driver_lambda(self, **kwargs):
        lambda_properties = self.config.get_config("enrol_driver_lambda_properties")

        lambda_permissions = [
            "dynamodb:PutItem",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_driver_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "EnrolDriverLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        enrol_driver_lambda = DeployLambdaStack(
            self,
            "EnrolDriverLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return enrol_driver_lambda

    def create_enrol_driver_api(self, **kwargs):
        api_properties = self.config.get_config("enrol_driver_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.enrol_driver_lambda.lambda_function

        enrol_driver_api = ApiGatewayStack(
            self,
            "EnrolDriverApi",
            api_properties,
            **kwargs,
        )

        return enrol_driver_api

    def create_get_driver_details_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_driver_details_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_driver_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetDriverDetailsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_driver_details_lambda = DeployLambdaStack(
            self,
            "GetDriverDetailsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_driver_details_lambda

    def create_get_driver_details_api(self, **kwargs):
        api_properties = self.config.get_config("get_driver_details_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.get_driver_details_lambda.lambda_function

        get_driver_details_api = ApiGatewayStack(
            self,
            "GetDriverDetailsApi",
            api_properties,
            **kwargs,
        )

        return get_driver_details_api

    def create_enrol_bus_ddb_table(self, **kwargs):
        ddb_table = DynamoDBStack(
            self,
            "EnrolBusDDBTable",
            self.config.get_config("enrol_bus_ddb_properties"),
            **kwargs,
        )
        return ddb_table

    def create_enrol_bus_lambda(self, **kwargs):
        lambda_properties = self.config.get_config("enrol_bus_lambda_properties")

        lambda_permissions = [
            "dynamodb:PutItem",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_bus_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "EnrolBusLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        enrol_bus_lambda = DeployLambdaStack(
            self,
            "EnrolBusLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return enrol_bus_lambda

    def create_enrol_bus_api(self, **kwargs):
        api_properties = self.config.get_config("enrol_bus_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.enrol_bus_lambda.lambda_function

        enrol_bus_api = ApiGatewayStack(
            self,
            "EnrolBusApi",
            api_properties,
            **kwargs,
        )

        return enrol_bus_api

    def create_get_bus_details_lambda(self, **kwargs):
        lambda_properties = self.config.get_config("get_bus_details_lambda_properties")

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_bus_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetBusDetailsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_bus_details_lambda = DeployLambdaStack(
            self,
            "GetBusDetailsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_bus_details_lambda

    def create_get_bus_details_api(self, **kwargs):
        api_properties = self.config.get_config("get_bus_details_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.get_bus_details_lambda.lambda_function

        get_bus_details_api = ApiGatewayStack(
            self,
            "GetBusDetailsApi",
            api_properties,
            **kwargs,
        )

        return get_bus_details_api

    def create_enrol_route_ddb_table(self, **kwargs):
        ddb_table = DynamoDBStack(
            self,
            "EnrolRouteDDBTable",
            self.config.get_config("enrol_route_ddb_properties"),
            **kwargs,
        )
        return ddb_table

    def create_enrol_route_lambda(self, **kwargs):
        lambda_properties = self.config.get_config("enrol_route_lambda_properties")

        lambda_permissions = [
            "dynamodb:PutItem",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_route_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "EnrolRouteLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        enrol_route_lambda = DeployLambdaStack(
            self,
            "EnrolRouteLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return enrol_route_lambda

    def create_enrol_route_api(self, **kwargs):
        api_properties = self.config.get_config("enrol_route_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.enrol_route_lambda.lambda_function

        enrol_route_api = ApiGatewayStack(
            self,
            "EnrolRouteApi",
            api_properties,
            **kwargs,
        )

        return enrol_route_api

    def create_get_route_details_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_route_details_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_route_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetRouteDetailsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_route_details_lambda = DeployLambdaStack(
            self,
            "GetRouteDetailsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_route_details_lambda

    def create_get_route_details_api(self, **kwargs):
        api_properties = self.config.get_config("get_route_details_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.get_route_details_lambda.lambda_function

        get_route_details_api = ApiGatewayStack(
            self,
            "GetRouteDetailsApi",
            api_properties,
            **kwargs,
        )

        return get_route_details_api

    def create_associate_driver_bus_route_ddb_table(self, **kwargs):
        ddb_table = DynamoDBStack(
            self,
            "AssociateDriverBusRouteDDBTable",
            self.config.get_config("associate_driver_bus_route_ddb_properties"),
            **kwargs,
        )
        return ddb_table

    def create_associate_driver_bus_route_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "associate_driver_bus_route_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:PutItem",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.associate_driver_bus_route_ddb_table.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "AssociateDriverBusRouteLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        associate_driver_bus_route_lambda = DeployLambdaStack(
            self,
            "AssociateDriverBusRouteLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return associate_driver_bus_route_lambda

    def create_get_driver_bus_route_association_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_driver_bus_route_association_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.associate_driver_bus_route_ddb_table.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetDriverBusRouteAssociationLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_driver_bus_route_association_lambda = DeployLambdaStack(
            self,
            "GetDriverBusRouteAssociationLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_driver_bus_route_association_lambda

    def create_associate_driver_bus_route_api(self, **kwargs):
        api_properties = self.config.get_config(
            "associate_driver_bus_route_apigw_properties"
        )

        api_properties["integration"][
            "lambda_function"
        ] = self.associate_driver_bus_route_lambda.lambda_function

        associate_driver_bus_route_api = ApiGatewayStack(
            self,
            "AssociateDriverBusRouteApi",
            api_properties,
            **kwargs,
        )

        return associate_driver_bus_route_api

    def create_get_driver_bus_route_association_api(self, **kwargs):
        api_properties = self.config.get_config(
            "get_driver_bus_route_association_apigw_properties"
        )

        api_properties["integration"][
            "lambda_function"
        ] = self.get_route_bus_driver_association_lambda.lambda_function

        get_driver_bus_route_association_api = ApiGatewayStack(
            self,
            "GetDriverBusRouteAssociationApi",
            api_properties,
            **kwargs,
        )

        return get_driver_bus_route_association_api

    
    def create_get_route_bus_driver_association_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_driver_bus_route_association_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.associate_driver_bus_route_ddb_table.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetRouteBusDriverAssociationLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_route_bus_driver_association_lambda = DeployLambdaStack(
            self,
            "GetRouteBusDriverAssociationLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_route_bus_driver_association_lambda

    def create_get_route_bus_driver_association_api(self, **kwargs):
        api_properties = self.config.get_config(
            "get_driver_bus_route_association_apigw_properties"
        )

        api_properties["integration"][
            "lambda_function"
        ] = self.get_route_bus_driver_association_lambda.lambda_function

        get_route_bus_driver_association_api = ApiGatewayStack(
            self,
            "GetRouteBusDriverAssociationApi",
            api_properties,
            **kwargs,
        )

        return get_route_bus_driver_association_api

    def create_get_all_driver_details_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_all_driver_details_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_driver_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetAllDriverDetailsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_all_driver_details_lambda = DeployLambdaStack(
            self,
            "GetAllDriverDetailsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_all_driver_details_lambda

    def create_get_all_driver_details_api(self, **kwargs):
        api_properties = self.config.get_config(
            "get_all_driver_details_apigw_properties"
        )

        api_properties["integration"][
            "lambda_function"
        ] = self.get_all_driver_details_lambda.lambda_function

        get_all_driver_details_api = ApiGatewayStack(
            self,
            "GetAllDriverDetailsApi",
            api_properties,
            **kwargs,
        )

        return get_all_driver_details_api

    def create_get_all_bus_details_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_all_bus_details_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_bus_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetAllBusDetailsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_all_bus_details_lambda = DeployLambdaStack(
            self,
            "GetAllBusDetailsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_all_bus_details_lambda

    def create_get_all_bus_details_api(self, **kwargs):
        api_properties = self.config.get_config("get_all_bus_details_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.get_all_bus_details_lambda.lambda_function

        get_all_bus_details_api = ApiGatewayStack(
            self,
            "GetAllBusDetailsApi",
            api_properties,
            **kwargs,
        )

        return get_all_bus_details_api

    def create_get_all_route_details_lambda(self, **kwargs):
        lambda_properties = self.config.get_config(
            "get_all_route_details_lambda_properties"
        )

        lambda_permissions = [
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.enrol_route_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GetAllRouteDetailsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        get_all_route_details_lambda = DeployLambdaStack(
            self,
            "GetAllRouteDetailsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return get_all_route_details_lambda

    def create_get_all_route_details_api(self, **kwargs):
        api_properties = self.config.get_config(
            "get_all_route_details_apigw_properties"
        )

        api_properties["integration"][
            "lambda_function"
        ] = self.get_all_route_details_lambda.lambda_function

        get_all_route_details_api = ApiGatewayStack(
            self,
            "GetAllRouteDetailsApi",
            api_properties,
            **kwargs,
        )

        return get_all_route_details_api

    
    def create_google_maps_lambda(self, **kwargs):
        lambda_properties = self.config.get_config("google_maps_wrapper_lambda_properties")

        lambda_permissions = [
            "dynamodb:PutItem",
        ] + self.cw_logs_permissions

        lambda_resources = [
            self.geo_location_ddb.get_ddb_table_arn
        ] + self.cw_logs_resources

        lambda_policy_statement = [
            iam.PolicyStatement(
                actions=lambda_permissions,
                resources=lambda_resources,
            ),
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"],
            ),
        ]

        lambda_role = Iam(
            self,
            "GoogleMapsLambdaRole",
            assumed_by="lambda.amazonaws.com",
            policy_statements=lambda_policy_statement,
        ).get_role

        google_maps_lambda = DeployLambdaStack(
            self,
            "GoogleMapsLambda",
            lambda_properties,
            lambda_role,
            **kwargs,
        )

        return google_maps_lambda
    
    def create_google_maps_api(self, **kwargs):
        api_properties = self.config.get_config("google_maps_wrapper_apigw_properties")

        api_properties["integration"][
            "lambda_function"
        ] = self.google_maps_lambda.lambda_function

        google_maps_api = ApiGatewayStack(
            self,
            "GoogleMapsApi",
            api_properties,
            **kwargs,
        )

        return google_maps_api
