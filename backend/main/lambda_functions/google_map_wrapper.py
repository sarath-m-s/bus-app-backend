import json

import requests

from backend.main.lambda_layer.python.constants import *


def lambda_handler(event, context):
    if event["queryStringParameters"] and "origin_lat" in event["queryStringParameters"] and "origin_lng" in event["queryStringParameters"] and "destination_lat" in event["queryStringParameters"] and "destination_lng" in event["queryStringParameters"]:
        origin_lat = event['queryStringParameters']['origin_lat']
        origin_lng = event['queryStringParameters']['origin_lng']
        destination_lat = event['queryStringParameters']['destination_lat']
        destination_lng = event['queryStringParameters']['destination_lng']

        destination = event['queryStringParameters']['destination']
        api_key = GOOGLE_MAPS_API_KEY

        response = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={origin_lat},{origin_lng}&destination={destination_lat},{destination_lng}&key={api_key}')

        headers = {
            'Access-Control-Allow-Origin': '*',  # This allows all origins. Adjust as needed for your use case.
            'Access-Control-Allow-Credentials': True,
        }

        if response.status_code == 200:
            return {
                'statusCode': 200,
                'body': json.dumps(response.json()),
                'headers': headers
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to fetch directions'}),
                'headers': headers
            }