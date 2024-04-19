# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module exposes Panopto "RemoteRecorderManagement" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException
from itertools import count


class RemoteRecorderManagement(PanoptoAPI):
    def __init__(self):
        super(RemoteRecorderManagement, self).__init__(
            wsdl='RemoteRecorderManagement.svc?wsdl',
            port='BasicHttpBinding_IRemoteRecorderManagement')

    def recorder_settings(self, recorder_id):
        obj = self._instance('ns0:ArrayOfRecorderSettings')
        obj.RecorderSettings.append(self._instance('ns0:RecorderSettings'))
        obj.RecorderSettings[0].RecorderId = recorder_id
        return obj

    def getRemoteRecordersById(self, remote_recorder_id):
        return self._request('GetRemoteRecordersById', {
            'remoteRecorderIds': self.guid_list(
                ns='ns4:ArrayOfguid', guids=[remote_recorder_id]),
        })

    def getRemoteRecordersByExternalId(self, external_id):
        return self._request('GetRemoteRecordersByExternalId', {
            'externalIds': self.parameter_list(params=[external_id]),
        })

    def scheduleRecording(self, name, folder_id, is_broadcast,
                          start_time, end_time, recorder_id):
        return self._request('ScheduleRecording', {
            'name': name,
            'folderId': folder_id,
            'isBroadcast': is_broadcast,
            'start': start_time,
            'end': end_time,
            'recorderSettings': self.recorder_settings(recorder_id),
        })

    def listRecorders(self, sort_by='Name'):
        result = []

        self._set_max_results(100)
        for page in count(0):
            self._set_page_number(page)

            response = self._request('ListRecorders', {
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
            'externalId': external_id,
            'remoteRecorderId': remote_recorder_id
        })

    # UpdateRecordingTime(ns0:AuthenticationInfo auth, ns3:guid sessionId,
    # xs:dateTime start, xs:dateTime end)
    def updateRecordingTime(self, session_id, start, end):
        return self._request('UpdateRecordingTime', {
            'sessionId': session_id,
            'start': start,
            'end': end
        })

    # ScheduleRecurringRecording(ns0:AuthenticationInfo auth,
    # ns3:guid scheduledSessionId, ns2:ArrayOfDayOfWeek daysOfWeek,
    # xs:dateTime end)
