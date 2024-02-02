from pathlib import Path
from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as iam
from constructs import Construct
from aws_cdk import Duration


class DeployLambdaStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        lambda_properties: dict,
        iam_role: iam.Role,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        Lambda properties JSON Structure:
        {
            "lambda_function": {
                "function_name": "LambdaFunctionName",
                "asset_path": "LambdaFunctionAssetPath",
                "handler": "LambdaFunctionHandler",
                "runtime": "LambdaFunctionRuntime",
                "timeout": "LambdaFunctionTimeout",
                "memory_size": "LambdaFunctionMemorySize",
                "environment_variables": "LambdaFunctionEnvironmentVariables",
                "description": "LambdaFunctionDescription"
            },
            "lambda_layer": {
                "asset_path": "LambdaLayerAssetPath",
                "layer_name": "LambdaLayerName",
                "description": "LambdaLayerDescription"
            },
            "event_source_mapping_properties": {
                "event_source_arn": "EventSourceArn"
            }
        }
        
        """
        self._lambda_function = None

        self.lambda_properties = lambda_properties
        self.lambda_function_properties = self.lambda_properties["lambda_function"]
        self.function_name = self.lambda_function_properties["function_name"]
        self.function_asset_path = self.lambda_function_properties["asset_path"]
        self.handler = self.lambda_function_properties["handler"]
        self.runtime = _lambda.Runtime(self.lambda_function_properties["runtime"])
        self.max_retries = self.lambda_function_properties.get("max_retries", 1)
        self.timeout = Duration.seconds(
            self.lambda_function_properties.get("timeout", 3)
        )
        self.memory_size = self.lambda_function_properties.get("memory_size", 128)
        self.environment_variables = self.lambda_function_properties.get(
            "environment_variables", None
        )
        self.description = self.lambda_function_properties["description"]
        self.role = iam_role
        self.lambda_layer_properties = self.lambda_properties.get("lambda_layer", None)
        self.layer_asset_path = self.lambda_layer_properties.get("asset_path", None)
        self.layer_name = self.lambda_layer_properties.get("layer_name", None)
        self.description = self.lambda_layer_properties.get("description", None)
        self.lambda_event_source_mapping_properties = self.lambda_properties.get(
            "event_source_mapping_properties", None
        )
        if self.lambda_event_source_mapping_properties:
            self.event_source_arn = self.lambda_event_source_mapping_properties.get(
                "event_source_arn", None
            )

        # deploy lambda function
        if self.lambda_layer_properties:
            self._lambda_function = self.deploy_lambda()
            self.lambda_layer = self.lambda_layer(
                self.layer_name, self.layer_asset_path, self.description
            )
            self.lambda_function.add_layers(self.lambda_layer)
        else:
            self._lambda_function = self.deploy_lambda()

        # deploy lambda event source mapping
        if self.lambda_event_source_mapping_properties:
            self.lambda_event_source_mapping(self.lambda_function)

    def deploy_lambda(self, layers=None):
        lambda_function = _lambda.Function(
            self,
            self.function_name,
            function_name=self.function_name,
            code=_lambda.Code.from_asset(str(Path.cwd() / self.function_asset_path)),
            handler=self.handler,
            runtime=self.runtime,
            timeout=self.timeout,
            retry_attempts=self.max_retries,
            memory_size=self.memory_size,
            environment=self.environment_variables,
            description=self.description,
            role=self.role,
            layers=self.lambda_layer if layers else None,
        )
        return lambda_function

    def lambda_layer(self, layer_name, layer_asset_path, description=None):
        return _lambda.LayerVersion(
            self,
            layer_name,
            code=_lambda.Code.from_asset(str(Path.cwd() / self.layer_asset_path)),
            # compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
            description=description,
        )

    def lambda_event_source_mapping(self, lambda_function):
        return _lambda.EventSourceMapping(
            self,
            "EventSourceMappingId",
            target=lambda_function,
            event_source_arn=self.event_source_arn,
            batch_size=1,
        )

    @property
    def lambda_function(self):
        return self._lambda_function

    @lambda_function.setter
    def lambda_function(self, value):
        self._lambda_function = value

    # arn
    @property
    def lambda_function_arn(self):
        return self.lambda_function.function_arn
