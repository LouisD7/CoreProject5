import json

class event_service:
    def __init__(self, event):
        self.event = event

    def event_parser(self):       
        print(self.event)
        print("smello")
        if self.event.get('httpMethod') == 'GET':
            print("GET request received")
            print(self.event.get('patientID'))

        elif self.event.get('httpMethod') == 'POST':
            print("POST request received")

        elif self.event.get('httpMethod') == 'PUT':
            print("PUT request received")

        elif self.event.get('httpMethod') == 'DELETE':
            print("DELETE request received")
        