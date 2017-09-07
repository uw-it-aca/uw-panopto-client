"""
Panopto API mock data class
"""
from commonconf import settings
from importlib import import_module
from logging import getLogger
from hashlib import md5
import sys
import os
import re
from os.path import abspath, dirname


class PanoptoMockData(object):
    # Based on django.template.loaders.app_directories
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    app_resource_dirs = []

    def __init__(self):
        self._log = getLogger(__name__)

        if len(PanoptoMockData.app_resource_dirs) < 1:
            for app in getattr(settings, 'INSTALLED_APPS', []):
                try:
                    mod = import_module(app)
                except ImportError as ex:
                    raise ImproperlyConfigured('ImportError %s: %s' % (
                        app, ex.args[0]))

                resource_dir = os.path.join(os.path.dirname(mod.__file__),
                                            'resources/panopto/file')
                if os.path.isdir(resource_dir):
                    # Cheating, to make sure our resources are overridable
                    data = {
                        'path': resource_dir.decode(
                            PanoptoMockData.fs_encoding),
                        'app': app,
                    }
                    PanoptoMockData.app_resource_dirs.insert(0, data)

    def mock(self, portName, methodName, params):
        mock_path = self._mock_file_path(portName, methodName, params)
        for resource in PanoptoMockData.app_resource_dirs:
            mock_data = self._load_mock_resource_from_path(resource, mock_path)
            if mock_data:
                return mock_data

        return ''

    def _load_mock_resource_from_path(self, resource_dir, resource_path):
        orig_file_path = os.path.join(resource_dir['path'], resource_path)

        paths = [
            self.convert_to_platform_safe(orig_file_path),
        ]

        file_path = None
        handle = None
        for path in paths:
            try:
                file_path = path
                handle = open(path)
                break
            except IOError as ex:
                pass

        if handle is None:
            return None

        mock_data = handle.read()
        handle.close()

        return mock_data

    def _mock_file_path(self, portName, methodName, params):
        return os.path.join(portName, methodName,
                            md5(self._normalize(params)).hexdigest().upper())

    def _normalize(self, params):
        ignored = ['auth']
        normalized = {}

        for k in sorted(params.keys()):
            if k not in ignored:
                normalized[k] = params[k]

        return str(normalized)

    def convert_to_platform_safe(self, dir_file_name):
        """
        :param dir_file_name: a string to be processed
        :return: a string with all the reserved characters replaced
        """
        return re.sub('[\?|<>=:*,;+&"@]', '_', dir_file_name)
