"""
This module exposes Panopto "AccessManagement" Service methods
"""
from django.conf import settings
from panopto_client import PanoptoAPI, PanoptoAPIException



class AccessManagement(PanoptoAPI):
    def __init__(self):
        super(AccessManagement, self).__init__({
            'wsdl': 'https://%s/Panopto/PublicAPI/4.6/AccessManagement.svc?wsdl' % (settings.PANOPTO_SERVER)
        })
        self._port = 'BasicHttpBinding_IAccessManagement'

    def getFolderAccessDetails(self, folder_id):
        id = self._api.factory.create('ns1:guid')
        id = folder_id

        return self._request('GetFolderAccessDetails',
                             {
                                 'auth': self.authentication_info(),
                                 'folderId': folder_id,
                             })

    def grantUsersAccessToFolder(self, folder_id, user_ids, role):
        userIds = self._api.factory.create('ns2:ArrayOfguid')
        userIds.guid = user_ids

        return self._request('GrantUsersAccessToFolder',
                             {
                                 'auth': self.authentication_info(),
                                 'folderId': folder_id,
                                 'userIds': userIds,
                                 'role': role
                             })

    def revokeUsersAccessFromFolder(self, folder_id, user_ids, role):
        userIds = self._api.factory.create('ns2:ArrayOfguid')
        userIds.guid = user_ids

        return self._request('RevokeUsersAccessFromFolder',
                             {
                                 'auth': self.authentication_info(),
                                 'folderId': folder_id,
                                 'userIds': userIds,
                                 'role': role
                             })

    def getSessionAccessDetails(self, session_id):
        return self._request('GetSessionAccessDetails',
                             {
                                 'auth': self.authentication_info(),
                                 'sessionId': session_id
                             })

    def updateSessionIsPublic(self, session_id, is_public):
        return self._request('UpdateSessionIsPublic',
                             {
                                 'auth': self.authentication_info(),
                                 'sessionId': session_id,
                                 'isPublic': is_public
                             })
