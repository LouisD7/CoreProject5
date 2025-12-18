import json
from aws.event_service import event_service

def lambda_handler(event, context):
    
    handle_event = event_service(event)
    
    return handle_event
