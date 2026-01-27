import json
import boto3
from decimal import Decimal

class delete_patient_details():
    def __init__(self, event):
        self.event = event
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('PatientDataTable')

    def delete_patient_data(self):
        patient_id = self.event.get('queryStringParameters').get('patientID')
        if patient_id is None:
            return {
                'statusCode': 400,
                'body': 'No Patient ID in request'
            }
        try:
            if len(patient_id) != 6:
                return {
                    'statusCode': 400,
                    'body': 'Invalid patient ID Incorrect length'
                }
            patient_id = int(patient_id)
        except TypeError, ValueError:
            return {
                    'statusCode': 400,
                    'body': 'Invalid patient ID check format of patient ID'
                }
        print("before table response")
        self.table.delete_item(
            Key={
               'patientID': patient_id
           }
        )
        return {
            'statusCode': 200,
            'body': f"Deleted patient with ID of {patient_id}"
        }
        


