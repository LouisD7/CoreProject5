import unittest
import os
import json
from unittest.mock import Mock, patch
from aws.get_patient_details import get_patient_details
import test_variables

# decorator for mocking the dynamo table resource for testing as not to use the actual dynamo resource
def patch_boto(value):
    def mock_boto(func):
        def decorator_dynamo(*args, **kwargs):
            mock_table = Mock() # mocking the table resource from dynamo
            mock_boto = Mock() # mocking boto3 resource
            with patch("boto3.resource") as boto_resource_mock: # patching boto3.resource to use the mocked values
                boto_resource_mock.return_value = mock_boto # making the boto.resource.return_value be the mocked boto value
                mock_boto.Table.return_value = mock_table # making the mocked boto value = the mock dyanymo table
                mock_table.get_item.return_value = { # mocking the return get_item.return_value = the passed in object
                    "Item" : value
                }
                return func(*args, **kwargs)
        return decorator_dynamo
    return mock_boto

class TestEventService(unittest.TestCase):
    @patch_boto(test_variables.TABLE_ITEM)
    def test_get_request_happy_path_returns_200(self):
        event = get_patient_details(json_file_parser("json\\get_request.json"))
        response = event.get_patient_data()
        self.assertEqual(response, test_variables.HAPPY_GET_RESPONSE)

    @patch_boto(test_variables.TABLE_ITEM)
    def test_get_request_missing_patientID_returns_400(self):
        event = get_patient_details(json_file_parser("json\\get_request_missing_patientID.json"))
        response = event.get_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_GET_RESPONSE_MISSING_PATIENTID)

    @patch_boto(test_variables.TABLE_ITEM)
    def test_get_request_patientID_length_incorrect_returns_400(self):
        event = get_patient_details(json_file_parser("json\\get_request_incorrect_patientID_length.json"))
        response = event.get_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_GET_RESPONSE_INCORRECT_ID_LENGTH)

    @patch_boto(test_variables.TABLE_ITEM)
    def test_get_request_patientID_containes_non_numeric_characters_returns_400(self):
        event = get_patient_details(json_file_parser("json\\get_request_patientID_conatins_non_numeric_characters.json"))
        response = event.get_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_GET_RESPONSE_PATIENTID_CONTAINS_NON_NUMERIC_CHARACTERS)
    
    @patch_boto(test_variables.UNHAPPY_GET_TABLE_ITEM_INCORRECT_FORMAT)
    def test_get_request_dynamo_returns_non_dumpable_value_returns_400(self):
        event = get_patient_details(json_file_parser("json\\get_request.json"))
        with self.assertRaises(TypeError): #asserts that the code inside this with will return an TypeError exception
            response = event.get_patient_data()
            self.assertEqual(response, "TypeError: item 2000-07-07 00:00:00 is not a decimal")

def json_file_parser(file_path):
    json_file_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(json_file_path, 'r', encoding = "utf-8") as file:
        request_dict = json.loads(file.read())
    return request_dict
