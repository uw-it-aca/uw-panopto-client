# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Panopto API mock data class
"""
from commonconf import settings
from importlib import import_module
from hashlib import md5
import sys
import os
import re
import json
from os.path import abspath, dirname


class PanoptoMockData(object):
    # Based on django.template.loaders.app_directories
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    app_resource_dirs = []

    def __init__(self):
        if len(PanoptoMockData.app_resource_dirs) < 1:
            for app in getattr(settings, 'INSTALLED_APPS', []):
                try:
                    mod = import_module(app)
                except ModuleNotFoundError as ex:
                    mod = import_module('.'.join(app.split('.')[0:-1]))

                except ImportError as ex:
                    raise ImproperlyConfigured('ImportError {}: {}'.format(
                        app, ex.args[0]))

                resource_dir = os.path.join(os.path.dirname(mod.__file__),
                                            'resources/panopto/file')
                if os.path.isdir(resource_dir):
                    # Cheating, to make sure our resources are overridable
                    data = {
                        'path': resource_dir,
                        'app': app,
                    }
                    PanoptoMockData.app_resource_dirs.insert(0, data)

    def wsdl(self, path):
        for resource in PanoptoMockData.app_resource_dirs:
            resource_file = os.path.join(
                resource['path'], path.strip('/')).split('?', 1)[0]
            if os.stat(self.convert_to_platform_safe(resource_file)):
                return "file://{}".format(resource_file)

        return ''

    def mock(self, portName, methodName, params):
        mock_path = self._mock_file_path(portName, methodName, params)
        for resource in PanoptoMockData.app_resource_dirs:
            mock_data = self._load_mock_resource_from_path(resource, mock_path)
            if mock_data:
                return mock_data.encode('utf-8')

        return "".encode('utf-8')

    def _load_mock_resource_from_path(self, resource_dir, resource_path):
        orig_file_path = os.path.join(resource_dir['path'], resource_path)

        paths = [
            self.convert_to_platform_safe(orig_file_path),
        ]

        handle = None
        for path in paths:
            try:
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
        return os.path.join(portName, methodName, self._param_hash(params))

    def _normalized(self, params):
        excluded = {'auth'}
        return {k: params[k] for k in params if k not in excluded}

    def _param_hash(self, params):
        return md5(json.dumps(
            self._normalized(params),
            default=lambda o: re.sub(r"[\s]*", "", str(o)),
            sort_keys=True).encode()).hexdigest().upper()

    def convert_to_platform_safe(self, dir_file_name):
        """
        :param dir_file_name: a string to be processed
        :return: a string with all the reserved characters replaced
        """
        return re.sub(r'[\?|<>=:*,;+&"@]', '_', dir_file_name)
