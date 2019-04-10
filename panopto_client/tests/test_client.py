from unittest import TestCase
from commonconf import override_settings
from panopto_client import PanoptoAPI, PanoptoAPIException, URL_BASE


class PanoptoClientTest(TestCase):
    @override_settings(PANOPTO_SERVER='localhost')
    def test_init_mock(self):
        client = PanoptoAPI(wsdl='test_wsdl', port='test_port')
        self.assertEqual(client._panopto_server, 'localhost')
        self.assertEqual(
            client._wsdl, 'https://localhost{}/test_wsdl'.format(
                URL_BASE))
        self.assertEqual(client._port, 'test_port')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._mock)
        self.assertEqual(client._auth_user_key, '')
        self.assertEqual(client._auth_token, '')

    @override_settings(PANOPTO_SERVER='localhost',
                       PANOPTO_API_APP_ID='test-api-app-id',
                       PANOPTO_API_USER='test-api-user',
                       PANOPTO_API_TOKEN='test-api-token')
    def test_init_live(self):
        client = PanoptoAPI(wsdl='test_wsdl', port='test_port')
        self.assertEqual(client._port, 'test_port')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)
        self.assertEqual(
            client._auth_user_key, 'test-api-app-id\\test-api-user')
        self.assertEqual(client._auth_token, 'test-api-token')

    @override_settings(PANOPTO_SERVER='localhost')
    def test_api_attr(self):
        client = PanoptoAPI(wsdl='test_wsdl', port='test_port')

        # Nonexistent attribute fails normally
        self.assertRaises(AttributeError, getattr, client, '_fail')

        # Connection error
        self.assertRaises(PanoptoAPIException, hasattr, client, '_api')
        self.assertRaises(PanoptoAPIException, getattr, client, '_api')
