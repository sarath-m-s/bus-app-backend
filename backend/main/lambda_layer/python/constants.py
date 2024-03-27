APPLICATION_NAME = "bta"

# aws account details
AWS_ACCOUNT = "310160951350"
AWS_REGION = "us-east-1"

# Lambda
SAVE_INCOMING_GEO_LOCATION_LAMBDA = "save_incoming_geo_location"
GET_GEO_LOCATION_LAMBDA = "get_geo_location"
ENROL_DRIVER_LAMBDA = "enrol_driver"
GET_DRIVER_DETAILS_LAMBDA = "get_driver_details"
ENROL_BUS_LAMBDA = "enrol_bus"
GET_BUS_DETAILS_LAMBDA = "get_bus_details"
ENROL_ROUTE_LAMBDA = "enrol_route"
GET_ROUTE_DETAILS_LAMBDA = "get_route_details"
ASSOCIATE_DRIVER_BUS_ROUTE_LAMBDA = "associate_driver_bus_route"
GET_DRIVER_BUS_ROUTE_ASSOCIATION_LAMBDA = "get_driver_bus_route_association"
GET_ALL_DRIVER_DETAILS = "get_all_driver_details"
GET_ALL_BUS_DETAILS = "get_all_bus_details"
GET_ALL_ROUTE_DETAILS = "get_all_route_details"
GOOGLE_MAPS_WRAPPER_LAMBDA = "google_maps_wrapper"

# Dynamo DB
GEO_LOCATION_TABLE = "geo_location"
GEO_LOCATION_TABLE_PARTITION_KEY = "bus_id"
BUS_MASTER_TABLE = "bus_master"
BUS_MASTER_TABLE_PARTITION_KEY = "bus_id"
DRIVER_MASTER_TABLE = "driver_master"
DRIVER_MASTER_TABLE_PARTITION_KEY = "driver_id"
ROUTE_MASTER_TABLE = "route_master"
ROUTE_MASTER_TABLE_PARTITION_KEY = "route_id"
ASSOCIATION_TABLE = "association"
ASSOCIATION_TABLE_PARTITION_KEY = "association_id"

# API Gateway
SAVE_GEO_LOCATION_API_GATEWAY_NAME = "save_geo_location_api"
SAVE_GEO_LOCATION_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "save", "geo-location"]
GET_GEO_LOCATION_API_GATEWAY_NAME = "get_geo_location_api"
GET_GEO_LOCATION_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "get", "geo-location"]
ENROL_DRIVER_API_GATEWAY_NAME = "enrol_driver_api"
ENROL_DRIVER_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "enrol", "driver"]
GET_DRIVER_DETAILS_API_GATEWAY_NAME = "get_driver_details_api"
GET_DRIVER_DETAILS_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "get", "driver-details"]
ENROL_BUS_API_GATEWAY_NAME = "enrol_bus_api"
ENROL_BUS_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "enrol", "bus"]
GET_BUS_DETAILS_API_GATEWAY_NAME = "get_bus_details_api"
GET_BUS_DETAILS_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "get", "bus-details"]
ENROL_ROUTE_API_GATEWAY_NAME = "enrol_route_api"
ENROL_ROUTE_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "enrol", "route"]
GET_ROUTE_DETAILS_API_GATEWAY_NAME = "get_route_details_api"
GET_ROUTE_DETAILS_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "get", "route-details"]
ASSOCIATE_DRIVER_BUS_ROUTE_API_GATEWAY_NAME = "associate_bus_route_api"
ASSOCIATE_DRIVER_BUS_ROUTE_API_GATEWAY_PATH = [
    f"{APPLICATION_NAME}",
    "associate",
    "driver-bus-route",
]
GET_DRIVER_BUS_ROUTE_ASSOCIATION_API_GATEWAY_NAME = (
    "get_driver_bus_route_association_api"
)
GET_DRIVER_BUS_ROUTE_ASSOCIATION_API_GATEWAY_PATH = [
    f"{APPLICATION_NAME}",
    "get",
    "driver-bus-route-association",
]
GET_ALL_DRIVER_DETAILS_API_GATEWAY_NAME = "get_all_driver_details_api"
GET_ALL_DRIVER_DETAILS_API_GATEWAY_PATH = [
    f"{APPLICATION_NAME}",
    "get",
    "all-driver-details",
]
GET_ALL_BUS_DETAILS_API_GATEWAY_NAME = "get_all_bus_details_api"
GET_ALL_BUS_DETAILS_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "get", "all-bus-details"]
GET_ALL_ROUTE_DETAILS_API_GATEWAY_NAME = "get_all_route_details_api"
GET_ALL_ROUTE_DETAILS_API_GATEWAY_PATH = [
    f"{APPLICATION_NAME}",
    "get",
    "all-route-details",
]
GOOGLE_MAPS_WRAPPER_API_GATEWAY_NAME = "google_maps_wrapper_api"
GOOGLE_MAPS_WRAPPER_API_GATEWAY_PATH = [f"{APPLICATION_NAME}", "google-maps-wrapper"]


# IAM
CLOUDWATCH_LOGS_PERMISSIONS = [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents",
]
CLOUDWATCH_LOGS_RESOURCES = ["arn:aws:logs:*:*:*"]

#Google Maps 
GOOGLE_MAPS_API_KEY = "AIzaSyCCTN2hd3Ovs-yMeKTB0WeYBkMWm14MY7g"
