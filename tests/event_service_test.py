import unittest
import os
import json
from aws.event_service import event_service

class TestEventService(unittest.TestCase):

    def test_json_parsing(self):
        print("")

def json_file_parser(file_path):
    json_file_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(json_file_path, 'r', encoding = "utf-8") as file:
        reqeust_dict = json.loads(file.read)
    return reqeust_dict