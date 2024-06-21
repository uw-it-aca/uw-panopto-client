# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Base module to support exposing Panopto SOAP Service methods
"""
from commonconf import settings
from logging import getLogger
from suds.client import Client
from suds.xsd.schema import Schema
from suds import WebFault
from prometheus_client import Histogram, Counter
from panopto_client.mock_data import PanoptoMockData
from weakref import WeakValueDictionary
from hashlib import sha1
import time
import sys

URL_BASE = '/Panopto/PublicAPI/4.6'

# prepare for prometheus observations
prometheus_duration = Histogram('soapclient_request_duration_seconds',
                                'Soapclient request duration (seconds)',
                                ['method'])
prometheus_status = Histogram('soapclient_response_status_code',
                              'Soapclient request response status code',
                              ['method'],
                              buckets=[100, 200, 300, 400, 500])
prometheus_timeout = Counter('soapclient_request_timeout',
                             'Soapclient request timeout count',
                             ['method'])


class PanoptoAPIException(Exception):
    pass


#
# monkeypatch suds Schema class for circular wsdl import sensitivity
#
def schema_patch_init(self, root, baseurl, options, loaded_schemata=None,
                      container=None):
    self.instance_cache[baseurl] = self
    self.__schema_init__(root, baseurl, options, container=container)


def schema_patch_instance(self, root, baseurl, loaded_schemata, options):
    if baseurl not in self.instance_cache:
        self.instance_cache[baseurl] = Schema(root, baseurl, options)

    return self.instance_cache[baseurl]


setattr(Schema, 'instance_cache', WeakValueDictionary())
setattr(Schema, '__schema_init__', Schema.__init__)
setattr(Schema, '__init__', schema_patch_init)
setattr(Schema, 'instance', schema_patch_instance)


class PanoptoAPI(object):
    """Panopto API base
       For help, see: http://support.panopto.com/pages/PanoptoApiHelp
    """
    def __init__(self, wsdl='', port=None):
        if hasattr(settings, 'PANOPTO_SERVER'):
            self._panopto_server = settings.PANOPTO_SERVER.lower()
        else:
            self._panopto_server = 'localhost'

        self._log = getLogger('client')
        self._page_max_results = 100
        self._page_number = 0
        self._actas = None
        self._port = port

        if (getattr(settings, 'PANOPTO_API_APP_ID', None) is not None and
                getattr(settings, 'PANOPTO_API_USER', None) is not None and
                getattr(settings, 'PANOPTO_API_TOKEN', None) is not None):
            self._wsdl = 'https://{host}{path}/{wsdl}'.format(
                host=self._panopto_server, path=URL_BASE, wsdl=wsdl)
            self._data = self._live
            self._auth_user_key = '{}\\{}'.format(
                settings.PANOPTO_API_APP_ID, settings.PANOPTO_API_USER)
            self._auth_token = settings.PANOPTO_API_TOKEN
        else:
            self._wsdl = PanoptoMockData().wsdl('{path}/{wsdl}'.format(
                path=URL_BASE, wsdl=wsdl))
            self._data = self._mock
            self._auth_user_key = ''
            self._auth_token = ''

    def __getattr__(self, name, *args, **kwargs):
        if name == '_api':
            try:
                self._api = Client(self._wsdl)
                self._api.set_options(cachingpolicy=0)
                if self._data == self._mock:
                    self._api.set_options(nosend=True)
                    self._api.set_options(extraArgumentErrors=False)

                return self._api
            except Exception as err:
                raise PanoptoAPIException("Cannot connect to '{}': {}".format(
                    self._wsdl, err))

        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, name))

    def auth_user_key(self):
        if self._actas and len(self._actas):
            return self._actas

        return self._auth_user_key

    def auth_code(self):
        signed_payload = '{}@{}|{}'.format(
            self.auth_user_key(), self._panopto_server, self._auth_token)
        return sha1(signed_payload.encode('utf-8')).hexdigest().upper()

    def authentication_info(self, ns='ns0:AuthenticationInfo'):
        obj = self._instance(ns)
        obj.AuthCode = self.auth_code()
        obj.UserKey = self.auth_user_key()
        return obj

    def pagination(self, ns='ns0:Pagination'):
        obj = self._instance(ns)
        obj.MaxNumberResults = self._page_max_results
        obj.PageNumber = self._page_number
        return obj

    def parameter_list(self, ns='ns4:ArrayOfstring', params=[]):
        obj = self._instance(ns)
        obj.string = params
        return obj

    def guid_list(self, ns='ns2:ArrayOfguid', guids=[]):
        obj = self._instance(ns)
        obj.guid = guids
        return obj

    def _set_page_number(self, page_number):
        self._page_number = int(page_number)

    def _set_max_results(self, max_results):
        self._page_max_results = int(max_results)

    def _instance(self, namespace):
        return self._api.factory.create(namespace)

    def _request(self, methodName, params={}):
        if 'auth' not in params:
            params['auth'] = self.authentication_info()

        try:
            start_time = time.time()
            response = self._data(methodName, params)
            self.prometheus_duration(methodName, time.time() - start_time)
            return response
        except WebFault as err:
            self._log.exception(err)
            raise PanoptoAPIException("Cannot connect to '{}': {}".format(
                    self._wsdl, err))
        except Exception as err:
            self._log.error('Error: ({}) {}'.format(
                err, str(sys.exc_info()[0])))

            if type(err.args[0]) is tuple and type(err.args[0][0]) is int:
                self.prometheus_status(methodName, err.args[0][0])
                if err.args[0][0] in [401, 403]:
                    errmsg = 'The request cannot be authenticated ({})'.format(
                        err.args[0][0])
                if err.args[0][0] in [404, 405, 406, 500]:
                    errmsg = 'The server is currently unavailable ({})'.format(
                        err.args[0][0])
                else:
                    errmsg = 'Unanticipated error: {} ({})'.format(
                        err.args[0][1], err.args[0][0])
            else:
                self.prometheus_timeout(methodName)
                errmsg = 'Error connecting: {}'.format(err)

            raise PanoptoAPIException(errmsg)

    def _live(self, methodName, params={}):
        return self._api.service[self._port][methodName](**params)

    def _mock(self, methodName, params={}):
        params['__inject'] = {
            'reply': PanoptoMockData().mock(self._port, methodName, params)
        }
        return self._api.service[self._port][methodName](**params)

    def prometheus_duration(self, method, duration):
        prometheus_duration.labels(method).observe(duration)

    def prometheus_status(self, method, status):
        prometheus_status.labels(method).observe(
            (int(status) // 100) * 100)

    def prometheus_timeout(self, method):
        prometheus_timeout.labels(method).inc()
