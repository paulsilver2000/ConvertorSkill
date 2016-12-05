from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import time

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    print("event: " + json.dumps(event))
    print("getting username: "+json.dumps(event['params']['path']['customerid']))
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('accounts')

    customer_id = event['params']['path']['customerid']
    accounts = []

    response = table.scan()
    for item in response['Items']:
        if item['customer_id'] == customer_id:
            accounts.append(item)

    return accounts