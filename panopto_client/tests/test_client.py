# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from commonconf import override_settings
from panopto_client import PanoptoAPI, PanoptoAPIException, URL_BASE


@override_settings(PANOPTO_API_APP_ID=None,
                   PANOPTO_API_USER=None,
                   PANOPTO_API_TOKEN=None)
class PanoptoMockClientTest(TestCase):
    def test_init_mock(self):
        client = PanoptoAPI(wsdl='test_wsdl', port='test_port')
        self.assertEqual(client._data, client._mock)
        self.assertEqual(client._auth_user_key, '')
        self.assertEqual(client._auth_token, '')


class PanoptoLiveClientTest(TestCase):
    def test_init_live(self):
        client = PanoptoAPI(wsdl='test_wsdl', port='test_port')
        self.assertEqual(client._port, 'test_port')
        self.assertEqual(client._panopto_server, 'localhost')
        self.assertEqual(
            client._wsdl, 'https://localhost{}/test_wsdl'.format(
                URL_BASE))
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)
        self.assertEqual(
            client._auth_user_key, 'test-api-app-id\\test-api-user')
        self.assertEqual(client._auth_token, 'test-api-token')

    def test_api_attr(self):
        client = PanoptoAPI(wsdl='test_wsdl', port='test_port')

        # Nonexistent attribute fails normally
        self.assertRaises(AttributeError, getattr, client, '_fail')

        # Connection error
        self.assertRaises(PanoptoAPIException, hasattr, client, '_api')
        self.assertRaises(PanoptoAPIException, getattr, client, '_api')

    def test_auth_user_key(self):
        client = PanoptoAPI()
        self.assertEqual(
            client.auth_user_key(), 'test-api-app-id\\test-api-user')

        client._actas = 'javerage'
        self.assertEqual(client.auth_user_key(), 'javerage')

    def test_auth_code(self):
        client = PanoptoAPI()
        self.assertEqual(
            client.auth_code(), 'F23922FC14C8A8CF3AB37CD33FCC909202D338D8')
