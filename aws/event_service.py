from aws.get_patient_details import get_patient_details
from aws.delete_patient_details import delete_patient_details
from aws.post_patient_details import post_patient_details
from aws.put_patient_details import put_patient_details

class event_service():
    def __init__(self, event):
        self.event = event

    def event_parser(self):
        print(self.event)
        if self.event.get('httpMethod') == 'GET':
            return(get_patient_details(self.event).get_patient_data())

        elif self.event.get('httpMethod') == 'POST':
            return(post_patient_details(self.event).post_patient_data())

        elif self.event.get('httpMethod') == 'PUT':
            return(put_patient_details(self.event).put_patient_data())

        elif self.event.get('httpMethod') == 'DELETE':
            return(delete_patient_details(self.event).delete_patient_data())
