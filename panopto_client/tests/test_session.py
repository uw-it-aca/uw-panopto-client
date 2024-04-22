# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from panopto_client.session import SessionManagement, PanoptoAPIException
from panopto_client.tests import instance_args
import mock


@mock.patch.object(SessionManagement, '_instance',
                   return_value=mock.sentinel.instance)
@mock.patch.object(SessionManagement, '_request')
class SessionManagementTest(TestCase):
    def test_init(self, mock_request, mock_instance):
        client = SessionManagement()
        self.assertEqual(client._port, 'BasicHttpBinding_ISessionManagement')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_getFoldersList(self, mock_request, mock_instance):
        mock_request.TotalNumberResults = 0
        client = SessionManagement()
        try:
            result = client.getFoldersList(search_query='test query')
        except TypeError:
            pass
        self.assertEqual(
            instance_args(mock_instance.call_args_list), [
                'ns1:AuthenticationInfo',
                'ns1:FolderSortField',
                'ns1:ListFoldersRequest',
                'ns1:Pagination'])
        mock_request.assert_called_with('GetFoldersList', {
            'auth': mock.sentinel.instance,
            'request': mock.sentinel.instance,
            'searchQuery': 'test query'})

    def test_getAllFoldersByExternalId(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.getAllFoldersByExternalId(['test-external-id'])
        self.assertEqual(
            instance_args(mock_instance.call_args_list), [
                'ns1:AuthenticationInfo',
                'ns6:ArrayOfstring',
                'ns6:ArrayOfstring'])
        mock_request.assert_called_with('GetAllFoldersByExternalId', {
            'auth': mock.sentinel.instance,
            'folderExternalIds': mock.sentinel.instance,
            'providerNames': mock.sentinel.instance})

    def test_getFoldersWithExternalContextList(
            self, mock_request, mock_instance):
        mock_request.TotalNumberResults = 0
        client = SessionManagement()
        try:
            result = client.getFoldersWithExternalContextList(
                search_query='test query')
        except TypeError:
            pass
        self.assertEqual(
            instance_args(mock_instance.call_args_list), [
                'ns1:AuthenticationInfo',
                'ns1:FolderSortField',
                'ns1:ListFoldersRequest',
                'ns1:Pagination'])
        mock_request.assert_called_with('GetFoldersWithExternalContextList', {
            'auth': mock.sentinel.instance, 'request': mock.sentinel.instance,
            'searchQuery': 'test query'})

    def test_getFoldersByExternalId(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.getFoldersByExternalId(['test-external-id'])
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo', 'ns6:ArrayOfstring'])
        mock_request.assert_called_with('GetFoldersByExternalId', {
            'auth': mock.sentinel.instance,
            'folderExternalIds': mock.sentinel.instance})

    def test_addFolder(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.addFolder('test-folder-name')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('AddFolder', {
            'auth': mock.sentinel.instance, 'name': 'test-folder-name',
            'parentFolder': None, 'isPublic': 'false'})

    def test_updateFolderName(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.updateFolderName('test-folder-id', 'test-folder-name')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateFolderName', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id',
            'name': 'test-folder-name'})

    def test_updateFolderExternalId(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.updateFolderExternalId(
            'test-folder-id', 'test-external-id')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateFolderExternalId', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id',
            'externalId': 'test-external-id'})

    def test_updateFolderExternalIdWithProvider(self, mock_request,
                                                mock_instance):
        client = SessionManagement()
        result = client.updateFolderExternalIdWithProvider(
            'test-folder-id', 'test-external-id', 'test-provider-name')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateFolderExternalIdWithProvider', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id',
            'externalId': 'test-external-id',
            'SiteMembershipProviderName': 'test-provider-name'})

    def test_updateFolderDescription(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.updateFolderDescription(
            'test-folder-id', 'description')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateFolderDescription', {
            'auth': mock.sentinel.instance, 'folderId': 'test-folder-id',
            'description': 'description'})

    def test_provisionExternalCourse(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.provisionExternalCourse(
            'test course name', 'test-course-id')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns1:AuthenticationInfo'])
        mock_request.assert_called_with('ProvisionExternalCourse', {
            'auth': mock.sentinel.instance, 'name': 'test course name',
            'externalId': 'test-course-id'})

    def test_getSessionsById(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.getSessionsById(['test-session-id'])
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo', 'ns6:ArrayOfguid'])
        mock_request.assert_called_with('GetSessionsById', {
            'auth': mock.sentinel.instance,
            'sessionIds': mock.sentinel.instance})

    def test_getSessionsByExternalId(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.getSessionsByExternalId(['test-external-id'])
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo', 'ns6:ArrayOfstring'])
        mock_request.assert_called_with('GetSessionsByExternalId', {
            'auth': mock.sentinel.instance,
            'sessionExternalIds': mock.sentinel.instance})

    def test_updateSessionExternalId(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.updateSessionExternalId(
            'test-session-id', 'test-external-id')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateSessionExternalId', {
            'auth': mock.sentinel.instance, 'sessionId': 'test-session-id',
            'externalId': 'test-external-id'})

    def test_updateSessionOwner(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.updateSessionOwner('test-session-id', 'owner-key')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo', 'ns6:ArrayOfguid'])
        mock_request.assert_called_with('UpdateSessionOwner', {
            'auth': mock.sentinel.instance,
            'sessionIds': mock.sentinel.instance,
            'newOwnerUserKey': 'owner-key'})

    def test_updateSessionIsBroadcast(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.updateSessionIsBroadcast('test-session-id', False)
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateSessionIsBroadcast', {
            'auth': mock.sentinel.instance, 'sessionId': 'test-session-id',
            'isBroadcast': False})

    def test_moveSessions(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.moveSessions(['test-session-id'], 'test-folder-id')
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo', 'ns6:ArrayOfguid'])
        mock_request.assert_called_with('MoveSessions', {
            'auth': mock.sentinel.instance,
            'sessionIds': mock.sentinel.instance,
            'folderId': 'test-folder-id'})

    def test_deleteSessions(self, mock_request, mock_instance):
        client = SessionManagement()
        result = client.deleteSessions(['test-session-id'])
        self.assertEqual(instance_args(mock_instance.call_args_list),
                         ['ns1:AuthenticationInfo', 'ns6:ArrayOfguid'])
        mock_request.assert_called_with('DeleteSessions', {
            'auth': mock.sentinel.instance,
            'sessionIds': mock.sentinel.instance})
