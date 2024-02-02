APPLICATION_NAME = "bta"

# aws account details
AWS_ACCOUNT = "310160951350"
AWS_REGION = "us-east-1"

# Lambda
SAVE_INCOMING_GEO_LOCATION_LAMBDA = "save_incoming_geo_location"
GET_GEO_LOCATION_LAMBDA = "get_geo_location"

# Dynamo DB
GEO_LOCATION_TABLE = "geo_location"
GEO_LOCATION_TABLE_PARTITION_KEY = "bus_id"

# API Gateway
SAVE_GEO_LOCATION_API_GATEWAY_NAME = "save_geo_location_api"
SAVE_GEO_LOCATION_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "save", "geo-location"]
GET_GEO_LOCATION_API_GATEWAY_NAME = "get_geo_location_api"
GET_GEO_LOCATION_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "get", "geo-location"]


# IAM
CLOUDWATCH_LOGS_PERMISSIONS = [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents",
]
CLOUDWATCH_LOGS_RESOURCES = ["arn:aws:logs:*:*:*"]
