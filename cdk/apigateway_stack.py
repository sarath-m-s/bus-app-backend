from aws_cdk import aws_apigateway as apigw
from aws_cdk import Stack
from constructs import Construct


class ApiGatewayStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, api_properties: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gateway properties
        self.rest_api_name = api_properties["rest_api_name"]
        self.api_key_required = api_properties["api_key_required"]
        self.integration_type = api_properties["integration_type"]
        self.model_schema = api_properties.get("model_schema", None)
        if self.integration_type == "lambda":
            self.lambda_function = api_properties["lambda_function"]
        self.part_path = api_properties["part_path"]
        self.method = api_properties["method"]
        self.stage = api_properties["stage"]

        # Create an API Gateway
        self.chatbot_api = self.create_api_gateway()
        self.root_resource = self.get_root_resource()
        self.resource = self.add_resource(self.part_path)
        self.integration = self.lambda_integration(self.lambda_function)
        if self.model_schema:
            self.model = self.create_model(
                f"{self.rest_api_name}_model", self.model_schema
            )
        self.method = self.add_method(self.resource, self.method, self.integration)
        deployment = self.deploy_api_gateway()
        stage = self.add_stage(deployment)
        self.associate_stage(stage)

    def create_api_gateway(self):
        self.chatbot_api = apigw.RestApi(
            self,
            "ApiGatewayId",
            rest_api_name=self.rest_api_name,
            description="This is the API Gateway for the Chatbot",
        )
        return self.chatbot_api

    def get_root_resource(self):
        return self.chatbot_api.root

    def add_resource(self, path_part: list):
        for path in path_part:
            self.chatbot_api.root.add_resource(path)
        return self.chatbot_api.root.resource_for_path("/".join(path_part))

    def lambda_integration(self, lambda_function):
        if self.integration_type == "lambda":
            return apigw.LambdaIntegration(
                lambda_function,
                proxy=False,
                integration_responses=[
                    apigw.IntegrationResponse(
                        status_code="200",
                        response_templates={"application/json": ""},
                    )
                ],
            )

    def create_model(self, model_name, schema):
        return self.chatbot_api.add_model(
            model_name,
            content_type="application/json",
            schema=schema,
            description="This is the model for the Chatbot API Gateway",
        )

    def add_method(self, resource, method, integration, model=None):
        return resource.add_method(
            method,
            integration,
            request_models={"application/json": model},
            method_responses=[
                apigw.MethodResponse(
                    status_code="200",
                    response_models={"application/json": apigw.Model.EMPTY_MODEL},
                )
            ],
            api_key_required=self.api_key_required,
        )

    def deploy_api_gateway(self):
        return apigw.Deployment(
            self,
            "DeploymentId",
            api=self.chatbot_api,
            description="This is the deployment of the Chatbot API Gateway",
        )

    def add_stage(self, deployment):
        return apigw.Stage(
            self,
            "StageId",
            deployment=deployment,
            stage_name=self.stage,
            description="This is the stage of the Chatbot API Gateway",
        )

    # Associate the stage with the RestApi
    def associate_stage(self, stage):
        return self.chatbot_api.deployment_stage(stage)

    @property
    def get_api_gateway(self):
        return self.chatbot_api
