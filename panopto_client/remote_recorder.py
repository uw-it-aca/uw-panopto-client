"""
This module exposes Panopto "RemoteRecorderManagement" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException
from itertools import count


class RemoteRecorderManagement(PanoptoAPI):
    def __init__(self):
        super(RemoteRecorderManagement, self).__init__({
            'wsdl': 'RemoteRecorderManagement.svc?wsdl'
        })
        self._port = 'BasicHttpBinding_IRemoteRecorderManagement'

    def getRemoteRecordersById(self, remote_recorder_id):
        remoteRecorderIds = self._api.factory.create('ns4:ArrayOfguid')
        remoteRecorderIds.guid = [remote_recorder_id]

        return self._request('GetRemoteRecordersById', {
            'auth': self.authentication_info(),
            'remoteRecorderIds': remoteRecorderIds
        })

    def getRemoteRecordersByExternalId(self, external_id):
        externalIds = self._api.factory.create('ns4:ArrayOfstring')
        externalIds.string = [external_id]

        return self._request('GetRemoteRecordersByExternalId', {
            'auth': self.authentication_info(),
            'externalIds': externalIds
        })

    def scheduleRecording(self, name, folder_id, is_broadcast,
                          start_time, end_time, recorder_id):
        recorderSettings = self._api.factory.create(
            'ns0:ArrayOfRecorderSettings')
        recorderSettings.RecorderSettings.append(
            self._api.factory.create('ns0:RecorderSettings'))
        recorderSettings.RecorderSettings[0].RecorderId = recorder_id

        return self._request('ScheduleRecording', {
            'auth': self.authentication_info(),
            'name': name,
            'folderId': folder_id,
            'isBroadcast': is_broadcast,
            'start': start_time,
            'end': end_time,
            'recorderSettings': recorderSettings
        })

    def listRecorders(self, sort_by='Name'):
        result = []

        self._set_max_results(100)
        for page in count(0):
            self._set_page_number(page)

            response = self._request('ListRecorders', {
                'auth': self.authentication_info(),
                'pagination': self.pagination(),
                'sortBy': sort_by
            })

            if response.PagedResults:
                for f in response.PagedResults.RemoteRecorder:
                    result.append(f)

            if len(result) >= response.TotalResultCount:
                break

        return result

    def updateRemoteRecorderExternalId(self, remote_recorder_id, external_id):
        return self._request('UpdateRemoteRecorderExternalId', {
            'auth': self.authentication_info(),
            'externalId': external_id,
            'remoteRecorderId': remote_recorder_id
        })

    # UpdateRecordingTime(ns0:AuthenticationInfo auth, ns3:guid sessionId,
    # xs:dateTime start, xs:dateTime end)
    def updateRecordingTime(self, session_id, start, end):
        return self._request('UpdateRecordingTime', {
            'auth': self.authentication_info(),
            'sessionId': session_id,
            'start': start,
            'end': end
        })

    # ScheduleRecurringRecording(ns0:AuthenticationInfo auth,
    # ns3:guid scheduledSessionId, ns2:ArrayOfDayOfWeek daysOfWeek,
    # xs:dateTime end)
