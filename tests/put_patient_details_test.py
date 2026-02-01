import unittest
import os
import json
from unittest.mock import Mock, patch
from botocore import exceptions

from aws.put_patient_details import put_patient_details
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
                mock_table.put_item.side_effect = value
                return func(*args, **kwargs)
        return decorator_dynamo
    return mock_boto

class TestPutPaientDetails(unittest.TestCase):
    @patch_boto(None)
    def test_put_request_happy_path_returns_200(self):
        event = put_patient_details(json_file_parser("json\\post_request\\post_request.json"))
        response = event.put_patient_data()
        self.assertEqual(response, test_variables.HAPPY_PUT_RESPONSE)

    @patch_boto(get_botocore_exception())
    def test_post_request_unhappy_path_returns_409(self):
        event = put_patient_details(json_file_parser("json\\post_request\\post_request.json"))
        response = event.put_patient_data()
        self.assertEqual(response, test_variables.UNHAPPY_PUT_RESPONSE)

def json_file_parser(file_path):
    json_file_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(json_file_path, 'r', encoding = "utf-8") as file:
        request_dict = json.loads(file.read())
    return request_dict