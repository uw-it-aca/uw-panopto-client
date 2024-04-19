# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module exposes Panopto "UserManagement" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException
from itertools import count


class UserManagement(PanoptoAPI):
    def __init__(self):
        super(UserManagement, self).__init__(
            wsdl='UserManagement.svc?wsdl',
            port='BasicHttpBinding_IUserManagement')

    def listUsers(self, search_query='', sort_by='UserKey',
                  sort_increasing='true'):
        parameters = self._instance('ns0:ListUsersRequest')
        parameters.SortBy = self._instance('ns0:UserSortField')
        parameters.SortBy = sort_by,
        parameters.SortIncreasing = sort_increasing

        result = []

        self._set_max_results(100)
        for page in count(0):
            self._set_page_number(page)

            parameters.Pagination = self.pagination()

            response = self._request('ListUsers', {
                'parameters': parameters,
                'searchQuery': search_query
            })

            if response.PagedResults:
                for u in response.PagedResults.User:
                    result.append(u)

            if len(result) >= response.TotalResultCount:
                break

        return result

    def getUserByKey(self, user_key):
        return self._request('GetUserByKey', {
            'userKey': user_key
        })

    def getUsers(self, user_ids):
        return self._request('GetUsers', {
            'userIds': self.guid_list(guids=user_ids)
        })
