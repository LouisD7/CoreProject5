import json
from aws.event_service import event_service

def lambda_handler(event, context):
    print(event)
    print("smello")
    if event.get('httpMethod') == 'GET':
        print("GET request received")
        print(event.get('patientID'))


    elif event.get('httpMethod') == 'POST':
        print("POST request received")

    elif event.get('httpMethod') == 'PUT':
        print("PUT request received")

    elif event.get('httpMethod') == 'DELETE':
        print("DELETE request received")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
