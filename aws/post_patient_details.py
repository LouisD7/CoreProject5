import boto3
from botocore import exceptions
from aws.patient_item import patient_item

class post_patient_details():
    def __init__(self, event):
        self.event = event
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('PatientDataTable')

    def post_patient_data(self):
        request = self.event.get("queryStringParameters")
        patient = patient_item(**request)
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
            ConditionExpression="attribute_not_exists(patientID)" #checks to see if the patient data already exists throws an error
            )
        except exceptions.ClientError:
            return {
                'statusCode': 409, #conflict error
                'body': f"Item {patient.patientID} already exists"
            }
        return {
            'statusCode': 200,
            'body': f"Item {patient.patientID} successfuly added"
        }
