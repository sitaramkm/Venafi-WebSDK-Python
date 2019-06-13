import json
import vcert
import cryptography
import logging
import time
import string
from vcert import Connection, CertificateRequest, TPPConnection
#import requests
from os import environ
import boto3

dynamoDBClient = boto3.resource('dynamodb',region_name='us-west-2') #add dynamo dependency for future data managmement. 

logging.basicConfig(level=logging.INFO)

def main():
    print("main function ") # only for local tests

def connectToTPP(tppurl, tppusername, tpppassword, tpptoken):
    print("Connecting to TPP")
    # Get credentials from environment variables
    #token = environ.get('TOKEN')
    zone = environ.get("ZONE")
    # connection will be chosen automatically based on what arguments are passed,
    # If token is passed Venafi Cloud connection will be used. if user, password, and URL Venafi Platform (TPP) will
    # be used. If none, test connection will be used.
    conn = Connection(url=tppurl, token=tpptoken, user=tppusername, password=tpppassword)
    # If your TPP server certificate signed with your own CA or available only via proxy you can specify requests vars
    # conn = Connection(url=url, token=token, user=user, password=password,
    #                   http_request_kwargs={"verify": "/path/to/trust/bundle.pem"})

    print("Trying to ping url %s" % conn._base_url  )
    
    status = conn.ping()
    print("Server online: %s" % status)
    if not status:
        print('Server offline - exit')
        return
        exit(1)
    conn._get_policy_dn(zone)

def lambda_handler(event, context):
    """TPP Functions Lambda Handler
    {
    "tppurl": "https://<Replace with TPP Server URL>",
    "tppusername": "<Replace with Admin>",
    "tpppassword": "<Replace with password>",
    "tpptoken": "<apikey>"
    }
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    
    """

    
    tppurl = event['tppurl']
    tppusername = event['tppusername']
    tpppassword = event['tpppassword']
    tpptoken = event ['tpptoken']
    connectToTPP(tppurl, tppusername, tpppassword, tpptoken)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Success!!",
            # "location": ip.text.replace("\n", "")
        }),
    }
