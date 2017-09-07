"""
Base module to support exposing Panopto SOAP Service methods
"""
from commonconf import settings
from logging import getLogger
from suds.client import Client
from suds.xsd.schema import Schema
from suds import WebFault
from panopto_client.mock import PanoptoMockData
from weakref import WeakValueDictionary
from hashlib import sha1
import sys


url_base = '/Panopto/PublicAPI/4.6'


class PanoptoAPIException(Exception):
    pass


#
# monkeypatch suds Schema class for circular wsdl import sensitivity
#
def schema_patch_init(self, root, baseurl, options, container=None):
    self.instance_cache[baseurl] = self
    self.__schema_init__(root, baseurl, options, container=container)


def schema_patch_instance(self, root, baseurl, options):
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
    def __init__(self, options={}):
        if hasattr(settings, 'PANOPTO_SERVER'):
            self._panopto_server = settings.PANOPTO_SERVER.lower()
        else:
            self._panopto_server = 'localhost'

        self._wsdl = 'https://%s%s/%s' % (
            self._panopto_server, url_base, options.get('wsdl', ''))
        self._log = getLogger('client')
        self._api = Client(self._wsdl)
        self._api.set_options(cachingpolicy=0)
        self._page_max_results = 100
        self._page_number = 0
        self._actas = None

        if (hasattr(settings, 'PANOPTO_API_APP_ID') and
                hasattr(settings, 'PANOPTO_API_USER') and
                hasattr(settings, 'PANOPTO_API_TOKEN')):
            self._data = self._live
            self._auth_user_key = '%s\\%s' % (
                settings.PANOPTO_API_APP_ID, settings.PANOPTO_API_USER)
            self._auth_token = settings.PANOPTO_API_TOKEN
        else:
            self._api.set_options(nosend=True)
            self._api.set_options(extraArgumentErrors=False)
            self._data = self._mock
            self._auth_user_key = ''
            self._auth_token = ''

    def auth_user_key(self):
        if self._actas and len(self._actas):
            return self._actas

        return self._auth_user_key

    def _auth_code(self):
        payload = self.auth_user_key() + '@' + self._panopto_server
        signed_payload = payload + '|' + self._auth_token
        return sha1(signed_payload).hexdigest().upper()

    def authentication_instance(self):
        return self._api.factory.create('ns0:AuthenticationInfo')

    def authentication_info(self):
        auth = self.authentication_instance()
        auth.AuthCode = self._auth_code()
        auth.UserKey = self.auth_user_key()
        return auth

    def pagination_instance(self):
        return self._api.factory.create('ns0:Pagination')

    def pagination(self):
        pagination = self.pagination_instance()
        pagination.MaxNumberResults = self._page_max_results
        pagination.PageNumber = self._page_number
        return pagination

    def _set_page_number(self, page_number):
        self._page_number = int(page_number)

    def _set_max_results(self, max_results):
        self._page_max_results = int(max_results)

    def _request(self, methodName, params={}):
        try:
            return self._data(methodName, params)
        except WebFault as err:
            self._log.exception(err)
            raise PanoptoAPIException(
                'Cannot connect to the Panopto server: %s' % err)
        except Exception as err:
            self._log.error('Error: (%s) %s' % (err, str(sys.exc_info()[0])))

            if type(err.args[0]) is tuple and type(err.args[0][0]) is int:
                if err.args[0][0] in [401, 403]:
                    errmsg = 'The request cannot be authenticated (%s)' % (
                        err.args[0][0])
                if err.args[0][0] in [404, 405, 406, 500]:
                    errmsg = 'The server is currently unavailable (%s)' % (
                        err.args[0][0])
                else:
                    errmsg = 'Unanticipated error: %s (%s)' % (
                        err.args[0][1], err.args[0][0])
            else:
                errmsg = 'Error connecting: %s' % (err)

            raise PanoptoAPIException(errmsg)

    def _live(self, methodName, params={}):
        return self._api.service[self._port][methodName](**params)

    def _mock(self, methodName, params={}):
        params['__inject'] = {
            'reply': PanoptoMockData().mock(self._port, methodName, params)
        }
        return self._api.service[self._port][methodName](**params)
