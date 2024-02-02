from aws_cdk import Stack
from constructs import Construct
from .sqs_stack import SqsStack
from .lambda_stack import DeployLambdaStack
from .ddb_stack import DynamoDBStack
from .apigw_stack import ApiGatewayStack
from .eventbridge_stack import EventBridgeStack
from .config import Config
from .iam_stack import Iam
from .s3_stack import S3Stack
from .step_functions_stack import StepFunctionsStack
from aws_cdk import (
    aws_iam as iam,
    aws_stepfunctions_tasks as tasks,
    aws_stepfunctions as sfn,
)
from backend.main.lambda_layer.python.constants import (
    CLOUDWATCH_LOGS_PERMISSIONS,
    CLOUDWATCH_LOGS_RESOURCES,
)


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
