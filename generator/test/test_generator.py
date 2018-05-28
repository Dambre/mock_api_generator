import unittest

from generator import Generate
from listener.validators.messages import messages
from utils import json_validate


class GenerateTestCase(unittest.TestCase):
    '''
    This testcase tests if generator returns valid data
    '''
    def test_generated_data_validity(self):
        for message in messages.values():
            types = ['request', 'response']
            for _type in types:
                validation_object = message[_type]
                data = Generate().get_data(validation_object)
                valid, err = json_validate(data, validation_object)
                assert valid is True, err
