# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from panopto_client.user import UserManagement, PanoptoAPIException
from panopto_client.tests import instance_args
import mock


@mock.patch.object(UserManagement, '_instance',
                   return_value=mock.sentinel.instance)
@mock.patch.object(UserManagement, '_request')
class PanoptoUserManagementTest(TestCase):
    def test_init(self, mock_request, mock_instance):
        client = UserManagement()
        self.assertEqual(client._port, 'BasicHttpBinding_IUserManagement')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_listUsers(self, mock_request, mock_instance):
        client = UserManagement()
        try:
            result = client.listUsers(search_query='test query')
        except TypeError:
            pass
        self.assertEqual(instance_args(mock_instance.call_args_list), [
             'ns0:ListUsersRequest', 'ns0:Pagination', 'ns0:UserSortField'])
        mock_request.assert_called_with('ListUsers', {
            'parameters': mock.sentinel.instance, 'searchQuery': 'test query'})

    def test_getUserByKey(self, mock_request, mock_instance):
        client = UserManagement()
        result = client.getUserByKey('test-user-key')
        self.assertEqual(instance_args(mock_instance.call_args_list), [])
        mock_request.assert_called_with('GetUserByKey', {
            'userKey': 'test-user-key'})

    def test_getUsers(self, mock_request, mock_instance):
        client = UserManagement()
        result = client.getUsers(['test-user-id'])
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns2:ArrayOfguid'])
        mock_request.assert_called_with('GetUsers', {
            'userIds': mock.sentinel.instance})
