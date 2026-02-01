from aws.event_service import event_service

def lambda_handler(event, context):
    
    try:
        handle_event = event_service(event)
        return handle_event.event_parser()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f" Unexpected error occured {e}"
        }
