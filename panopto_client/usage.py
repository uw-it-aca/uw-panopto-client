"""
This module exposes Panopto "UserReporting" Service methods
"""
from panopto_client import PanoptoAPI, PanoptoAPIException
from itertools import count


class UsageReporting(PanoptoAPI):
    def __init__(self):
        super(UsageReporting, self).__init__({
            'wsdl': 'UsageReporting.svc?wsdl'
        })
        self._port = 'BasicHttpBinding_IUsageReporting'

    def getUserDetailedUsage(self, user_id):
        result = []

        self._set_max_results(100)
        for page in count(0):
            self._set_page_number(page)

            response = self._request('GetUserDetailedUsage', {
                'auth': self.authentication_info(),
                'userId': user_id,
                'pagination': self.pagination()
            })

            if response.PagedResponses:
                for u in response.PagedResponses.DetailedUsageResponseItem:
                    result.append(u)

            if len(result) >= response.TotalNumberResponses:
                break

        return result
