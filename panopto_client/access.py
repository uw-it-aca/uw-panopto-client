# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module exposes Panopto "AccessManagement" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException


class AccessManagement(PanoptoAPI):
    def __init__(self):
        super(AccessManagement, self).__init__(
            wsdl='AccessManagement.svc?wsdl',
            port='BasicHttpBinding_IAccessManagement')

    def access_role(self, role):
        try:
            return self._instance('ns0:AccessRole')[role]
        except TypeError:
            return role

    def getFolderAccessDetails(self, folder_id):
        return self._request('GetFolderAccessDetails', {
            'folderId': folder_id,
        })

    def grantUsersAccessToFolder(self, folder_id, user_ids, role):
        return self._request('GrantUsersAccessToFolder', {
            'folderId': folder_id,
            'userIds': self.guid_list(ns='ns2:ArrayOfguid', guids=user_ids),
            'role': self.access_role(role),
        })

    def revokeUsersAccessFromFolder(self, folder_id, user_ids, role):
        return self._request('RevokeUsersAccessFromFolder', {
            'folderId': folder_id,
            'userIds': self.guid_list(ns='ns2:ArrayOfguid', guids=user_ids),
            'role': self.access_role(role),
        })

    def getSessionAccessDetails(self, session_id):
        return self._request('GetSessionAccessDetails', {
            'sessionId': session_id
        })

    def updateSessionIsPublic(self, session_id, is_public):
        return self._request('UpdateSessionIsPublic', {
            'sessionId': session_id,
            'isPublic': is_public
        })
