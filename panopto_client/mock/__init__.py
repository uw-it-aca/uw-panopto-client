"""
Panopto API mock data class
"""
from django.utils.log import getLogger
from hashlib import md5
import os.path



class PanoptoMockData(object):
    def __init__(self):
        self._log = getLogger('client')

    def mock(self, portName, methodName, params):
        try:
            fn = self.mock_file_path(portName, methodName, params)
            self._log.debug("mock data: %s" % fn)
            mock_data_file = open(fn, 'r')
            mock_data = mock_data_file.read()
            mock_data_file.close()
            return mock_data
        except Exception as ex:
            self._log.exception(ex)
            return ''


    def mock_file_path(self, portName, methodName, params):
        cwd = os.path.dirname(os.path.realpath(__file__))
        mock_data_filename = md5(self._normalize(params)).hexdigest().upper()
        return os.path.join(cwd, 'data', portName, methodName, mock_data_filename)

    def _normalize(self, params):
        ignored = ['auth']
        normalized = {}

        for k in params.keys():
            if k not in ignored:
                normalized[k] = params[k]

        return str(normalized)
