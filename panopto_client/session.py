# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module exposes Panopto "SessionManagement" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException
from itertools import count


class SessionManagement(PanoptoAPI):
    auth_ns = 'ns1:AuthenticationInfo'
    param_ns = 'ns6:ArrayOfstring'
    guid_ns = 'ns6:ArrayOfguid'

    def __init__(self):
        super(SessionManagement, self).__init__(
            wsdl='SessionManagement.svc?wsdl',
            port='BasicHttpBinding_ISessionManagement')

    def getFoldersList(
            self, search_query='', sort_by='Name', sort_increasing='true'):
        return self._folder_search('GetFoldersList', search_query,
                                   sort_by, sort_increasing)

    def getFoldersWithExternalContextList(
            self, search_query='', sort_by='Name', sort_increasing='true'):
        return self._folder_search('GetFoldersWithExternalContextList',
                                   search_query, sort_by, sort_increasing)

    def _folder_search(
            self, method, search_query='', sort_by='Name',
            sort_increasing='true'):
        request = self._instance('ns1:ListFoldersRequest')
        request.ParentFolderId = None
        request.PublicOnly = 'false'
        request.SortBy = self._instance('ns1:FolderSortField')
        request.SortBy = sort_by,
        request.SortIncreasing = sort_increasing

        result = []

        self._set_max_results(100)
        for page in count(0):
            self._set_page_number(page)

            request.Pagination = self.pagination(ns='ns1:Pagination')

            response = self._request(method, {
                'auth': self.authentication_info(ns=self.auth_ns),
                'request': request,
                'searchQuery': search_query
            })

            if not response:
                break

            if response.Results:
                for f in response.Results.Folder:
                    result.append(f)

            if len(result) >= response.TotalNumberResults:
                break

        return result

    def getAllFoldersWithExternalContextByExternalId(
            self, folder_external_ids, provider_names=[]):
        return self._request('GetAllFoldersWithExternalContextByExternalId', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderExternalIds': self.parameter_list(
                ns=self.param_ns, params=folder_external_ids),
            'providerNames': self.parameter_list(
                ns=self.param_ns, params=provider_names),
        })

    def getAllFoldersByExternalId(self, folder_external_ids,
                                  provider_names=[]):
        return self._request('GetAllFoldersByExternalId', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderExternalIds': self.parameter_list(
                ns=self.param_ns, params=folder_external_ids),
            'providerNames': self.parameter_list(
                ns=self.param_ns, params=provider_names),
        })

    def getFoldersByExternalId(self, folder_external_ids):
        return self._request('GetFoldersByExternalId', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderExternalIds': self.parameter_list(
                ns=self.param_ns, params=folder_external_ids),
        })

    def addFolder(self, folder_name):
        return self._request('AddFolder', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'name': folder_name,
            'parentFolder': None,
            'isPublic': 'false'
        })

    def updateFolderName(self, folder_id, name):
        return self._request('UpdateFolderName', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderId': folder_id,
            'name': name
        })

    def updateFolderExternalId(self, folder_id, external_id):
        return self._request('UpdateFolderExternalId', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderId': folder_id,
            'externalId': external_id
        })

    def updateFolderExternalIdWithProvider(
            self, folder_id, external_id, site_membership_provider_name):
        return self._request('UpdateFolderExternalIdWithProvider', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderId': folder_id,
            'externalId': external_id,
            'SiteMembershipProviderName': site_membership_provider_name
        })

    def updateFolderDescription(self, folder_id, description):
        return self._request('UpdateFolderDescription', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'folderId': folder_id,
            'description': description
        })

    def provisionExternalCourse(self, course_name, course_id):
        return self._request('ProvisionExternalCourse', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'name': course_name,
            'externalId': course_id
        })

    def getSessionsById(self, session_ids):
        return self._request('GetSessionsById', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionIds': self.guid_list(ns=self.guid_ns, guids=session_ids),
        })

    def getSessionsByExternalId(self, session_external_ids):
        return self._request('GetSessionsByExternalId', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionExternalIds': self.parameter_list(
                ns=self.param_ns, params=session_external_ids),
        })

    def updateSessionExternalId(self, session_id, external_id):
        return self._request('UpdateSessionExternalId', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionId': session_id,
            'externalId': external_id
        })

    def updateSessionOwner(self, session_id, new_owner_user_key):
        return self._request('UpdateSessionOwner', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionIds': self.guid_list(ns=self.guid_ns, guids=[session_id]),
            'newOwnerUserKey': new_owner_user_key
        })

    def updateSessionIsBroadcast(self, session_id, is_broadcast):
        return self._request('UpdateSessionIsBroadcast', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionId': session_id,
            'isBroadcast': is_broadcast
        })

    def moveSessions(self, session_ids, folder_id):
        return self._request('MoveSessions', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionIds': self.guid_list(ns=self.guid_ns, guids=session_ids),
            'folderId': folder_id
        })

    def deleteSessions(self, session_ids):
        return self._request('DeleteSessions', {
            'auth': self.authentication_info(ns=self.auth_ns),
            'sessionIds': self.guid_list(ns=self.guid_ns, guids=session_ids),
        })
