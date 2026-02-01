import unittest
import os
import json
from unittest.mock import Mock, patch
from botocore import exceptions

from aws.delete_patient_details import delete_patient_details
import test_variables

def get_botocore_exception():
    return exceptions.ClientError({
        "Error": {
            "Code": "ParameterNotFound","Message": "Parameter was not found"
            }
        },
    'get_parameter'
    )

def patch_boto(value):
    def mock_boto(func):
        def decorator_dynamo(*args, **kwargs):
            mock_table = Mock()
            mock_boto = Mock()
            with patch("boto3.resource") as boto_resource_mock:
                boto_resource_mock.return_value = mock_boto
                mock_boto.Table.return_value = mock_table
                mock_table.delete_item.side_effect = value
                return func(*args, **kwargs)
        return decorator_dynamo
    return mock_boto

class TestDeletePatientDetails(unittest.TestCase):
    @patch_boto(None)
    def test_delete_patients_details_happy_path_returns_200(self):
        event = delete_patient_details(json_file_parser("json\\get_request\\get_request.json"))
        response = event.delete_patient_data()
        self.assertEqual(response, test_variables.HAPPY_DELETE_RESPONSE)
    
    @patch_boto(get_botocore_exception())
    def test_delete_patient_details_patient_doesnt_exist_returns_200(self):
        event = delete_patient_details(json_file_parser("json\\get_request\\get_request.json"))
        response = event.delete_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_DELETE_RESPONSE_PATIENT_DOESNT_EXIST)

    @patch_boto(None)
    def test_delete_patient_details_patientID_is_none_returns_400(self):
        event = delete_patient_details(json_file_parser("json\\get_request\\get_request_missing_patientID.json"))
        response = event.delete_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_DELETE_RESPONSE_PATIENTID_IS_NONE)

    @patch_boto(None)
    def test_delete_patient_details_patientID_is_incorrect_length_400(self):
        event = delete_patient_details(json_file_parser("json\\get_request\\get_request_incorrect_patientID_length.json"))
        response = event.delete_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_DELETE_RESPONSE_PATIENTID_INCORRECT_LENGTH)

    @patch_boto(None)
    def test_delete_patient_details_patientID_contains_non_numeric_400(self):
        event = delete_patient_details(json_file_parser("json\\get_request\\get_request_patientID_conatins_non_numeric_characters.json"))
        response = event.delete_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_DELETE_RESPONSE_PATIENTID_CONTAINS_NON_NUMERIC_CHARACTERS)

def json_file_parser(file_path):
    json_file_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(json_file_path, 'r', encoding = "utf-8") as file:
        request_dict = json.loads(file.read())
    return request_dict