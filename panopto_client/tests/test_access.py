# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from panopto_client.access import AccessManagement, PanoptoAPIException
from panopto_client.tests import instance_args
import mock


@mock.patch.object(AccessManagement, '_instance',
                   return_value=mock.sentinel.instance)
@mock.patch.object(AccessManagement, '_request')
class PanoptoAccessTest(TestCase):
    def test_init(self, mock_request, mock_instance):
        client = AccessManagement()
        self.assertEqual(client._port, 'BasicHttpBinding_IAccessManagement')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_getFolderAccessDetails(self, mock_request, mock_instance):
        client = AccessManagement()
        result = client.getFolderAccessDetails('test-folder-id')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns0:AuthenticationInfo'])
        mock_request.assert_called_with('GetFolderAccessDetails', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id'})

    def test_grantUsersAccessToFolder(self, mock_request, mock_instance):
        client = AccessManagement()
        result = client.grantUsersAccessToFolder(
            'test-folder-id', ['user-id-1'], 'test-role')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AccessRole', 'ns0:AuthenticationInfo', 'ns2:ArrayOfguid'])
        mock_request.assert_called_with('GrantUsersAccessToFolder', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id',
            'userIds': mock.sentinel.instance, 'role': 'test-role'})

    def test_revokeUsersAccessFromFolder(self, mock_request, mock_instance):
        client = AccessManagement()
        result = client.revokeUsersAccessFromFolder(
            'test-folder-id', ['user-id-1'], 'test-role')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AccessRole', 'ns0:AuthenticationInfo', 'ns2:ArrayOfguid'])
        mock_request.assert_called_with('RevokeUsersAccessFromFolder', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id',
            'userIds': mock.sentinel.instance, 'role': 'test-role'})

    def test_getSessionAccessDetails(self, mock_request, mock_instance):
        client = AccessManagement()
        result = client.getSessionAccessDetails('test-session-id')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns0:AuthenticationInfo'])
        mock_request.assert_called_with('GetSessionAccessDetails', {
            'auth': mock.sentinel.instance, 'sessionId': 'test-session-id'})

    def test_updateSessionIsPublic(self, mock_request, mock_instance):
        client = AccessManagement()
        result = client.updateSessionIsPublic('test-session-id', True)
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns0:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateSessionIsPublic', {
            'auth': mock.sentinel.instance, 'sessionId': 'test-session-id',
            'isPublic': True})
