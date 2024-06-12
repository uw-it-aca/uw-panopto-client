# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from panopto_client.usage import UsageReporting, PanoptoAPIException
from panopto_client.tests import instance_args
import mock


@mock.patch.object(UsageReporting, '_instance',
                   return_value=mock.sentinel.instance)
@mock.patch.object(UsageReporting, '_request')
class PanoptoUsageTest(TestCase):
    def test_init(self, mock_request, mock_instance):
        client = UsageReporting()
        self.assertEqual(client._port, 'BasicHttpBinding_IUsageReporting')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_getUserDetailedUsage(self, mock_request, mock_instance):
        client = UsageReporting()
        try:
            result = client.getUserDetailedUsage('test-user-id')
        except TypeError:
            pass
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:Pagination'])
        mock_request.assert_called_with('GetUserDetailedUsage', {
             'userId': 'test-user-id', 'pagination': mock.sentinel.instance})
