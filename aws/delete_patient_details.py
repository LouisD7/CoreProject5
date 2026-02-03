import boto3
from botocore import exceptions

class delete_patient_details():
    def __init__(self, event):
        self.event = event
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('PatientDataTable')

    def delete_patient_data(self):
        patient_id = self.event.get('queryStringParameters', {}).get('patientID')
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
        except (TypeError, ValueError):
            return {
                    'statusCode': 400,
                    'body': 'Invalid patient ID check format of patient ID'
                }
        try:
            self.table.delete_item(
                Key={
                'patientID': patient_id
            },
            ConditionExpression="attribute_exists(patientID)" #checks to see if the patient data exists throws an error if it doesnt
            )
        except exceptions.ClientError:
            return {
                'statusCode': 404,
                'body': f"Item {patient_id} doesn't exist"
            }
        return {
            'statusCode': 200,
            'body': f"Deleted patient with ID of {patient_id}"
        }
        


