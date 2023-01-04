import os
import sys
import unittest
from unittest import mock
import pytest
from pathlib import Path

p = Path(os.path.dirname(__file__)+"/")
geomart_eggfile = str(list(p.glob('*.egg'))[0])
sys.path.append(geomart_eggfile)


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\', '')))

if not os.path.dirname(__file__) == "":
    os.chdir(os.path.dirname(__file__))

from agol_events import get_agol_event_list
from agol_events import get_secret_key_details
from agol_events import set_transaction_variables
from agol_events import get_config_settings
from agol_events import set_response_values
from agol_events import event_list
from agol_events import invokeLambda



from geomart.geomart_log_transaction import LogTransaction



class events(unittest.TestCase):
    # test class to unit test job status
    def setUp(self):
        self.region = "region"
        self.host = "host"
        self.profile = "profile"
        self.environment = 'LOCAL'
        self.withPathFileName = 'app.cfg'
        self.request_data = { 
                                "transactionID" : "User_Details",
                                "transactionLogName" : "API_CALLER"
                            }
        self.application_variable_dict = get_config_settings(self.withPathFileName)
        self.transaction_variables = set_transaction_variables(self.request_data, self.application_variable_dict)
        self.response_message = {}
        self.status ="Completed"
        self.statusCode = "s001" 
        self.statusMsg = "Unittest completed"


    @mock.patch("agol_events.AwsSecretManger")
    def test_get_agol_event_list(self, mock_aws):
        """ this method is used to test read agol data and get the events list """
        log_transaction = LogTransaction( self.transaction_variables[0],self.transaction_variables[1],  self.transaction_variables[2])
        with self.assertRaises(Exception):
            value = get_agol_event_list(self.application_variable_dict, log_transaction)
            self.assertIsNotNone(value)


    def test_get_config_settings(self ):
        """ this method is to test reading app config file """
        application_variable_dict = get_config_settings(self.withPathFileName)
        self.assertIsNotNone(application_variable_dict)

        self.withPathFileName_1 = ''
        with self.assertRaises(Exception):
            get_config_settings(self.withPathFileName_1)

    def test_set_response_values(self):
        """ this method is used to test set response json object """
        log_transaction = LogTransaction( self.transaction_variables[0],self.transaction_variables[1],  self.transaction_variables[2])
        valid = set_response_values(log_transaction, self.response_message, self.status, self.statusCode, self.statusMsg)
        self.assertEqual(valid,True)


    def test_set_transaction_variables(self ):
        """ this method is used to test set transaction variables  for application logging """
        value = set_transaction_variables(self.request_data, self. application_variable_dict)
        self.assertIsNotNone(value)


    @mock.patch("agol_events.AwsSecretManger")
    def test_get_secret_key_details(self, mock_aws):
        """ this method is used to test read secret key values """
        log_transaction = LogTransaction( self.transaction_variables[0],self.transaction_variables[1],  self.transaction_variables[2])
        value = get_secret_key_details(self.application_variable_dict, log_transaction)
        self.assertIsNotNone(value)
		

    @mock.patch("agol_events.AwsSecretManger")
    def test_event_list(self, mock_aws):
        """ this method to is used to test main method of API call which till perform actions according to request and sends back the response """
        value = event_list(self.request_data)
        self.assertIsNotNone(value)

        self.request_data_1 = { }
        # with self.assertRaises(Exception):
        value_err = event_list(self.request_data_1)
        self.assertIsNotNone(value_err)

    
    def test_invokeLambda(self):
        """ this method to is used to test main method of API call which till perform actions according to request and sends back the response """
        value = invokeLambda(self.request_data, None)
        self.assertIsNotNone(value)