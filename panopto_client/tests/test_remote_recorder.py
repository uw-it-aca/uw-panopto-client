from unittest import TestCase
from panopto_client.remote_recorder import (
    RemoteRecorderManagement, PanoptoAPIException)
from panopto_client.tests import instance_args
from datetime import datetime
import mock


@mock.patch.object(RemoteRecorderManagement, '_instance',
                   return_value=mock.sentinel.instance)
@mock.patch.object(RemoteRecorderManagement, '_request')
class RemoteRecorderManagementTest(TestCase):
    def test_init(self, mock_request, mock_instance):
        client = RemoteRecorderManagement()
        self.assertEqual(
            client._port, 'BasicHttpBinding_IRemoteRecorderManagement')
        self.assertEqual(client._actas, None)
        self.assertEqual(client._data, client._live)

    def test_getRemoteRecordersById(self, mock_request, mock_instance):
        client = RemoteRecorderManagement()
        result = client.getRemoteRecordersById('test-recorder-id')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AuthenticationInfo', 'ns4:ArrayOfguid'])
        mock_request.assert_called_with('GetRemoteRecordersById', {
            'auth': mock.sentinel.instance,
            'remoteRecorderIds': mock.sentinel.instance})

    def test_getRemoteRecordersByExternalId(self, mock_request, mock_instance):
        client = RemoteRecorderManagement()
        result = client.getRemoteRecordersByExternalId('test-external-id')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AuthenticationInfo', 'ns4:ArrayOfstring'])
        mock_request.assert_called_with('GetRemoteRecordersByExternalId', {
            'auth': mock.sentinel.instance,
            'externalIds': mock.sentinel.instance})

    def test_scheduleRecording(self, mock_request, mock_instance):
        mock.sentinel.instance.RecorderSettings = []
        client = RemoteRecorderManagement()
        result = client.scheduleRecording(
            'test-name', folder_id='test-folder-id', is_broadcast=False,
            start_time=datetime(2013, 3, 15, 9, 0, 0),
            end_time=datetime(2013, 3, 15, 10, 0, 0),
            recorder_id='test-recorder-id')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:ArrayOfRecorderSettings', 'ns0:AuthenticationInfo',
            'ns0:RecorderSettings'])
        mock_request.assert_called_with('ScheduleRecording', {
            'auth': mock.sentinel.instance, 'name': 'test-name',
            'folderId': 'test-folder-id', 'isBroadcast': False,
            'start': datetime(2013, 3, 15, 9, 0),
            'end': datetime(2013, 3, 15, 10, 0),
            'recorderSettings': mock.sentinel.instance})

    def test_listRecorders(self, mock_request, mock_instance):
        client = RemoteRecorderManagement()
        try:
            result = client.listRecorders()
        except TypeError:
            pass
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AuthenticationInfo', 'ns0:Pagination'])
        mock_request.assert_called_with('ListRecorders', {
            'auth': mock.sentinel.instance,
            'pagination': mock.sentinel.instance, 'sortBy': 'Name'})

    def test_updateRemoteRecorderExternalId(self, mock_request, mock_instance):
        client = RemoteRecorderManagement()
        result = client.updateRemoteRecorderExternalId(
            'test-recorder-id', 'test-external-id')
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateRemoteRecorderExternalId', {
            'auth': mock.sentinel.instance, 'externalId': 'test-external-id',
            'remoteRecorderId': 'test-recorder-id'})

    def test_updateRecordingTime(self, mock_request, mock_instance):
        client = RemoteRecorderManagement()
        result = client.updateRecordingTime(
            'test-session-id', start=datetime(2013, 3, 15, 9, 0, 0),
            end=datetime(2013, 3, 15, 10, 0, 0))
        self.assertEqual(instance_args(mock_instance.call_args_list), [
            'ns0:AuthenticationInfo'])
        mock_request.assert_called_with('UpdateRecordingTime', {
            'auth': mock.sentinel.instance, 'sessionId': 'test-session-id',
            'start': datetime(2013, 3, 15, 9, 0),
            'end': datetime(2013, 3, 15, 10, 0)})
