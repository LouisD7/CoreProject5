import json
import boto3
from decimal import Decimal

class get_patient_details():
    def __init__(self, event):
        self.event = event
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('PatientDataTable')

    def get_patient_data(self):
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
        response = self.table.get_item(
            Key={
               'patientID': patient_id
           }
        )
        item = response['Item']
        print("after table response")
        print(item)
        return {
            'statusCode': 200,
            'body': json.dumps(item, default=decimal_serializer)
        }
        #return(patient_id)
        #return the status code plox with item dumped

#This converst decimal values inside of the table item so the table item can be converted to json
def decimal_serializer(obj):
    
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f'item {obj} is not a decimal')
