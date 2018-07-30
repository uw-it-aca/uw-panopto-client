"""
This module exposes Panopto "SessionManagement" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException
from itertools import count


class SessionManagement(PanoptoAPI):
    def __init__(self):
        super(SessionManagement, self).__init__({
            'wsdl': 'SessionManagement.svc?wsdl'
        })
        self._port = 'BasicHttpBinding_ISessionManagement'

    # override for auth and pagination types
    def authentication_instance(self):
        return self._api.factory.create('ns1:AuthenticationInfo')

    def pagination_instance(self):
        return self._api.factory.create('ns1:Pagination')

    def getFoldersList(self, search_query='', sort_by='Name',
                       sort_increasing='true'):
        request = self._api.factory.create('ns1:ListFoldersRequest')
        request.ParentFolderId = None
        request.PublicOnly = 'false'
        request.SortBy = self._api.factory.create('ns1:FolderSortField')
        request.SortBy = sort_by,
        request.SortIncreasing = sort_increasing

        result = []

        self._set_max_results(100)
        for page in count(0):
            self._set_page_number(page)

            request.Pagination = self.pagination()

            response = self._request('GetFoldersList', {
                'auth': self.authentication_info(),
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

    def getAllFoldersByExternalId(self, folder_external_ids,
                                  provider_names=[]):
        folderExternalIds = self._api.factory.create('ns6:ArrayOfstring')
        folderExternalIds.string = folder_external_ids
        providerNames = self._api.factory.create('ns6:ArrayOfstring')
        providerNames.string = provider_names

        return self._request('GetAllFoldersByExternalId', {
            'auth': self.authentication_info(),
            'folderExternalIds': folderExternalIds,
            'providerNames': providerNames
        })

    def getFoldersByExternalId(self, folder_external_ids):
        folderExternalIds = self._api.factory.create('ns6:ArrayOfstring')
        folderExternalIds.string = folder_external_ids

        return self._request('GetFoldersByExternalId', {
            'auth': self.authentication_info(),
            'folderExternalIds': folderExternalIds
        })

    def addFolder(self, folder_name):
        return self._request('AddFolder', {
            'auth': self.authentication_info(),
            'name': folder_name,
            'parentFolder': None,
            'isPublic': 'false'
        })

    def updateFolderName(self, folder_id, name):
        return self._request('UpdateFolderName', {
            'auth': self.authentication_info(),
            'folderId': folder_id,
            'name': name
        })

    def updateFolderExternalId(self, folder_id, external_id):
        return self._request('UpdateFolderExternalId', {
            'auth': self.authentication_info(),
            'folderId': folder_id,
            'externalId': external_id
        })

    def updateFolderExternalIdWithProvider(
            self, folder_id, external_id, site_membership_provider_name):
        return self._request('UpdateFolderExternalIdWithProvider', {
            'auth': self.authentication_info(),
            'folderId': folder_id,
            'externalId': external_id,
            'SiteMembershipProviderName': site_membership_provider_name
        })

    def updateFolderDescription(self, folder_id, description):
        return self._request('UpdateFolderDescription', {
            'auth': self.authentication_info(),
            'folderId': folder_id,
            'description': description
        })

    def getSessionsById(self, session_ids):
        sessionIds = self._api.factory.create('ns6:ArrayOfguid')
        sessionIds.guid = session_ids

        return self._request('GetSessionsById', {
            'auth': self.authentication_info(),
            'sessionIds': sessionIds
        })

    def getSessionsByExternalId(self, session_external_ids):
        sessionExternalIds = self._api.factory.create('ns6:ArrayOfstring')
        sessionExternalIds.string = session_external_ids

        return self._request('GetSessionsByExternalId', {
            'auth': self.authentication_info(),
            'sessionExternalIds': sessionExternalIds
        })

    def updateSessionExternalId(self, session_id, external_id):
        return self._request('UpdateSessionExternalId', {
            'auth': self.authentication_info(),
            'sessionId': session_id,
            'externalId': external_id
        })

    def updateSessionOwner(self, session_id, new_owner_user_key):
        sessionIds = self._api.factory.create('ns6:ArrayOfguid')
        sessionIds.guid = [session_id]

        return self._request('UpdateSessionOwner', {
            'auth': self.authentication_info(),
            'sessionIds': sessionIds,
            'newOwnerUserKey': new_owner_user_key
        })

    def updateSessionIsBroadcast(self, session_id, is_broadcast):
        return self._request('UpdateSessionIsBroadcast', {
            'auth': self.authentication_info(),
            'sessionId': session_id,
            'isBroadcast': is_broadcast
        })

    def moveSessions(self, session_ids, folder_id):
        sessionIds = self._api.factory.create('ns6:ArrayOfguid')
        sessionIds.guid = session_ids

        return self._request('MoveSessions', {
            'auth': self.authentication_info(),
            'sessionIds': sessionIds,
            'folderId': folder_id
        })

    def deleteSessions(self, session_ids):
        sessionIds = self._api.factory.create('ns6:ArrayOfguid')
        sessionIds.guid = session_ids

        return self._request('DeleteSessions', {
            'auth': self.authentication_info(),
            'sessionIds': sessionIds
        })
