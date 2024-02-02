from aws_cdk import Stack, Duration
from constructs import Construct
from aws_cdk import aws_apigateway as apigw


class ApiGatewayStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, api_properties: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gateway properties
        self.rest_api_name = api_properties["rest_api_name"]
        self.api_key_required = api_properties["api_key_required"]
        self.integration = api_properties["integration"]
        self.part_path = api_properties["part_path"]
        self.method = api_properties["method"]
        self.timeout = api_properties.get("timeout", 29)

        # Create an API Gateway
        self.chatbot_api = apigw.RestApi(
            self,
            "ApiGatewayId",
            rest_api_name=self.rest_api_name,
            description="This is the API Gateway for the Chatbot",
        )

        self.root_resource = self.get_root_resource()
        self.resource = self.add_resource(self.part_path)
        self.integration = self.create_integration(self.integration)
        self.method = self.add_method(self.resource, self.method, self.integration)

    def create_integration(self, integration_properties):
        integration_type = integration_properties["type"]
        if integration_type == "lambda":
            lambda_function = integration_properties["lambda_function"]
            return apigw.LambdaIntegration(
                lambda_function,
                proxy=True,
            )
        elif integration_type == "sqs":
            sqs_queue = integration_properties["sqs_queue"]
            credentials_role = integration_properties["credentials_role"]
            integration = apigw.AwsIntegration(
                service="sqs",
                integration_http_method="POST",
                path="{}/{}".format(self.region, sqs_queue),
                options={
                    "credentials_role": credentials_role,
                    "request_parameters": {
                        "integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"
                    },
                    "request_templates": {
                        "application/json": "Action=SendMessage&MessageBody=$util.urlEncode($input.params().querystring)&QueueUrl=$util.urlEncode('https://sqs.{}/{}')".format(
                            self.region, sqs_queue
                        )
                    },
                    "integration_responses": [
                        {
                            "statusCode": "200",
                            "response_templates": {
                                "application/json": '{"success": true}'
                            },
                        }
                    ],
                },
            )
            return integration
        else:
            raise ValueError(f"Unsupported integration type: {integration_type}")

    def get_root_resource(self):
        return self.chatbot_api.root

    def add_resource(self, path_part: list):
        for path in path_part:
            self.chatbot_api.root.add_resource(path)
        resource = self.chatbot_api.root.resource_for_path("/".join(path_part))

        # Enable CORS
        resource.add_cors_preflight(
            allow_origins=["*"],
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
            allow_headers=["*"],
        )

        return resource

    def add_method(self, resource, method, integration):
        return resource.add_method(
            method,
            integration,
            method_responses=[
                apigw.MethodResponse(
                    status_code="200",
                    response_models={"application/json": apigw.Model.EMPTY_MODEL},
                )
            ],
            api_key_required=self.api_key_required,
        )

    @property
    def get_api_gateway(self):
        return self.chatbot_api

    @property
    def get_api_gateway_id(self):
        return self.chatbot_api.rest_api_id

    @property
    def get_api_gateway_url(self):
        return self.chatbot_api.url
