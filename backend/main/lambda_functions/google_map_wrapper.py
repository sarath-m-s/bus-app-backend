import json

import requests

from backend.main.lambda_layer.python.constants import *


def lambda_handler(event, context):
    if event["queryStringParameters"] and "origin" in event["queryStringParameters"] and "destination" in event["queryStringParameters"]:
        origin = event['queryStringParameters']['origin']
        destination = event['queryStringParameters']['destination']
        api_key = GOOGLE_MAPS_API_KEY

        response = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}')

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