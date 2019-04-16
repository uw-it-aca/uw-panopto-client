from unittest import TestCase
from commonconf import override_settings
from panopto_client.access import AccessManagement, PanoptoAPIException


@override_settings(PANOPTO_SERVER='localhost')
class PanoptoAccessLiveTest(TestCase):
    @override_settings(PANOPTO_API_APP_ID='test-api-app-id',
                       PANOPTO_API_USER='test-api-user',
                       PANOPTO_API_TOKEN='test-api-token')
    def test_init(self):
        client = AccessManagement()
        self.assertEqual(client._port, 'BasicHttpBinding_IAccessManagement')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_getFolderAccessDetails(self):
        client = AccessManagement()
        self.assertRaises(
            PanoptoAPIException, client.getFolderAccessDetails,
            'test_folder_id')

    def test_grantUsersAccessToFolder(self):
        client = AccessManagement()
        self.assertRaises(
            PanoptoAPIException, client.grantUsersAccessToFolder,
            'test_folder_id', ['user_id_1'], 'test_role')

    def test_revokeUsersAccessFromFolder(self):
        client = AccessManagement()
        self.assertRaises(
            PanoptoAPIException, client.revokeUsersAccessFromFolder,
            'test_folder_id', ['user_id_1'], 'test_role')

    def test_getSessionAccessDetails(self):
        client = AccessManagement()
        self.assertRaises(
            PanoptoAPIException, client.getSessionAccessDetails,
            'test_session_id')

    def test_updateSessionIsPublic(self):
        client = AccessManagement()
        self.assertRaises(
            PanoptoAPIException, client.updateSessionIsPublic,
            'test_session_id', True)
