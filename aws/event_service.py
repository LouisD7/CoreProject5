import json
from aws.get_patient_details import get_patient_details

class event_service:
    def __init__(self, event):
        self.event = event

    def event_parser(self):
        print(self.event)
        print("smello")
        if self.event.get('httpMethod') == 'GET':
            print("GET request received")
            print(self.event.get('patientID'))
            #return(self.event.get('queryStringParameters').get('patientID'))
            return(get_patient_details(self.event).get_patient_data())

        elif self.event.get('httpMethod') == 'POST':
            print("POST request received")

        elif self.event.get('httpMethod') == 'PUT':
            print("PUT request received")

        elif self.event.get('httpMethod') == 'DELETE':
            print("DELETE request received")

        return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
