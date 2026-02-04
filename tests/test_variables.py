from decimal import Decimal
import datetime

TABLE_ITEM = {'patientID': Decimal('300004'), 'Gender': 'Male', 'last_name': 'Morton', 'general_practice': 'Johnson, Tucker and Perry Medical Centre', 'GP_notes': {'2025-04-28': 'fatigue present for 2 weeks. Follow-up in next appointment.', '2025-05-30': 'Routine check-up. Elevated blood pressure noted.'}, 'home_address': '29 Griffin neck, Leonhaven, S4T 7WQ, UK', 'first_name': 'Hugh', 'phone_number': '+44798959802774', 'Age': Decimal('80')}

UNHAPPY_GET_TABLE_ITEM_INCORRECT_FORMAT = {'patientID': 300004, 'Gender': datetime.datetime(2000, 7, 7), 'last_name': 'Morton', 'general_practice': 'Johnson, Tucker and Perry Medical Centre', 'GP_notes': {'2025-04-28': 'fatigue present for 2 weeks. Follow-up in next appointment.', '2025-05-30': 'Routine check-up. Elevated blood pressure noted.'}, 'home_address': '29 Griffin neck, Leonhaven, S4T 7WQ, UK', 'first_name': 'Hugh', 'phone_number': '+44798959802774', 'Age': 80}

HAPPY_GET_RESPONSE =  {'statusCode': 200, 'body': '{"patientID": "300004", "Gender": "Male", "last_name": "Morton", "general_practice": "Johnson, Tucker and Perry Medical Centre", "GP_notes": {"2025-04-28": "fatigue present for 2 weeks. Follow-up in next appointment.", "2025-05-30": "Routine check-up. Elevated blood pressure noted."}, "home_address": "29 Griffin neck, Leonhaven, S4T 7WQ, UK", "first_name": "Hugh", "phone_number": "+44798959802774", "Age": "80"}'}

UNHAPPY_GET_RESPONSE_INCORRECT_ID_LENGTH = {'statusCode': 400, 'body': 'Invalid patient ID Incorrect length'}

UNHAPPY_GET_RESPONSE_MISSING_PATIENTID = {'statusCode': 400, 'body': 'No Patient ID in request'}

UNHAPPY_GET_RESPONSE_PATIENTID_CONTAINS_NON_NUMERIC_CHARACTERS = {'statusCode': 400, 'body': 'Invalid patient ID check format of patient ID'}

HAPPY_POST_RESPONSE = {
            'statusCode': 200,
            'body': "Item 300077 successfuly added"
        }

UNHAPPY_POST_RESPONSE = {
                'statusCode': 409, #conflict error
                'body': "Item 300077 already exists"
            }

HAPPY_DELETE_RESPONSE = {
            'statusCode': 200,
            'body': f"Deleted patient with ID of 300001"
        }

UNHAPPY_DELETE_RESPONSE_PATIENT_DOESNT_EXIST = {
                'statusCode': 404, #conflict error
                'body': "Item 300001 doesn't exist"
            }

UNHAPPY_DELETE_RESPONSE_PATIENTID_IS_NONE = {
                'statusCode': 400,
                'body': 'No Patient ID in request'
            }

UNHAPPY_DELETE_RESPONSE_PATIENTID_INCORRECT_LENGTH = {
                    'statusCode': 400,
                    'body': 'Invalid patient ID Incorrect length'
                }

UNHAPPY_DELETE_RESPONSE_PATIENTID_CONTAINS_NON_NUMERIC_CHARACTERS = {
                    'statusCode': 400,
                    'body': 'Invalid patient ID check format of patient ID'
                }

HAPPY_PUT_RESPONSE = {
            'statusCode': 200,
            'body': f"Item 300077 successfuly updated"
        }

UNHAPPY_PUT_RESPONSE = {
                'statusCode': 409, #conflict error
                'body': "Item 300077 doesn't exists"
            }
