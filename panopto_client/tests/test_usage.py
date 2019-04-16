from unittest import TestCase
from commonconf import override_settings
from panopto_client.usage import UsageReporting, PanoptoAPIException


@override_settings(PANOPTO_SERVER='localhost')
class PanoptoUsageLiveTest(TestCase):
    @override_settings(PANOPTO_API_APP_ID='test-api-app-id',
                       PANOPTO_API_USER='test-api-user',
                       PANOPTO_API_TOKEN='test-api-token')
    def test_init(self):
        client = UsageReporting()
        self.assertEqual(client._port, 'BasicHttpBinding_IUsageReporting')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_getUserDetailedUsage(self):
        client = UsageReporting()
        self.assertRaises(
            PanoptoAPIException, client.getUserDetailedUsage, 'test_user_id')
