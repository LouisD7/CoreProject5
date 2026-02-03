import boto3
import json
from botocore import exceptions
from aws.patient_item import patient_item

class put_patient_details():
    def __init__(self, event):
        self.event = event
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('PatientDataTable')

    def put_patient_data(self):
        request = self.event.get("body")
        patient = patient_item(**json.loads(request))
        patient.__post_init__()
        try:
            self.table.put_item(
            Item={
                'patientID': patient.patientID,
                'Age': patient.Age,
                'first_name': patient.first_name,
                'Gender': patient.Gender,
                'general_practice': patient.general_practice,
                'home_address': patient.home_address,
                'last_name': patient.last_name,
                'phone_number': patient.phone_number,
                'GP_notes': patient.GP_notes
            },
            ConditionExpression="attribute_exists(patientID)" #checks to see if the patient data exists
            )
        except exceptions.ClientError:
            return {
                'statusCode': 409, #conflict error
                'body': f"Item {patient.patientID} doesn't exists"
            }
        return {
            'statusCode': 200,
            'body': f"Item {patient.patientID} successfuly updated"
        }
