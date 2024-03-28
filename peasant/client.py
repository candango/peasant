# Copyright 2020-2024 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import logging
from peasant import get_version
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class PeasantTransport:

    _peasant: "Peasant"

    @property
    def peasant(self):
        return self._peasant

    @peasant.setter
    def peasant(self, peasant: "Peasant"):
        self._peasant = peasant

    def get(self, path, **kwargs):
        raise NotImplementedError

    def head(self, path, **kwargs):
        raise NotImplementedError

    def post(self, path, **kwargs):
        raise NotImplementedError

    def post_as_get(self, path, **kwargs):
        raise NotImplementedError

    def set_directory(self):
        raise NotImplementedError

    def new_nonce(self):
        raise NotImplementedError

    def is_registered(self):
        raise NotImplementedError


class Peasant(object):

    _transport: PeasantTransport

    def __init__(self, transport):
        self._directory_cache = None
        self._transport = transport
        self._transport.peasant = self

    @property
    def directory_cache(self):
        return self._directory_cache

    @directory_cache.setter
    def directory_cache(self, directory_cache):
        self._directory_cache = directory_cache

    @property
    def transport(self):
        return self._transport

    def directory(self):
        if self.directory_cache is None:
            self.transport.set_directory()
        return self.directory_cache

    def new_nonce(self):
        return self.transport.new_nonce()


class AsyncPeasant(Peasant):

    def __init__(self, transport):
        super(AsyncPeasant, self).__init__(transport)

    async def directory(self):
        if self._directory_cache is None:
            future = self.transport.set_directory()
            if future is not None:
                logger.debug("Running transport set directory cache "
                             "asynchronously.")
                await future
        return self._directory_cache


tornado_installed = False
try:
    from tornado.httpclient import HTTPRequest
    from tornado import version as tornado_version
    from tornado.httputil import url_concat
    from tornado.httpclient import AsyncHTTPClient, HTTPClientError
    tornado_installed = True

    def get_tornado_request(url, **kwargs):
        """ Return a HTTPRequest to help with AsyncHTTPClient and HTTPClient
        execution. The HTTPRequest will use the provided url combined with path
        if provided. The HTTPRequest method will be GET by default and can be
        changed if method is informed.
        If form_urlencoded is defined as True a Content-Type header will be
        added to the request with application/x-www-form-urlencoded value.

        :param str url: Base url to be set to the HTTPRequest
        :key form_urlencoded: If the true will add the header Content-Type
        application/x-www-form-urlencoded to the form. Default is False.
        :key method: Method to be used by the HTTPRequest. Default it GET.
        :key path: If informed will add the path to the base url informed.
        Default is None.
        :return HTTPRequest:
        """
        method = kwargs.get("method", "GET")
        path = kwargs.get("path", None)
        form_urlencoded = kwargs.get("form_urlencoded", False)
        if not url.endswith("/"):
            url = f"{url}/"
        if path is not None and path != "/":
            url = f"{url}{path}" % ()
        request = HTTPRequest(url, method=method)
        if form_urlencoded:
            request.headers.add("Content-Type",
                                "application/x-www-form-urlencoded")
        return request
except ImportError:
    pass


class TornadoTransport(PeasantTransport):

    def __init__(self, bastion_address):
        super().__init__()
        if not tornado_installed:
            logger.warn("TornadoTransport cannot be used without tornado "
                        "installed.\nIt is necessary to install peasant "
                        "with extras modifiers all or tornado.\n\n Ex: pip "
                        "install peasant[all] or pip install peasant[tornado]"
                        "\n\nInstalling tornado manually will also work.\n")
            raise NotImplementedError
        self._client = AsyncHTTPClient()
        self._bastion_address = bastion_address
        self._directory = None
        self.user_agent = (f"Peasant/{get_version()}"
                           f"Tornado/{tornado_version}")
        self._basic_headers = {
            'User-Agent': self.user_agent
        }

    def _get_path(self, path, **kwargs):
        query_string = kwargs.get('query_string')
        if query_string:
            path = url_concat(path, query_string)

    def _get_headers(self, **kwargs):
        headers = copy.deepcopy(self._basic_headers)
        _headers = kwargs.get('headers')
        if _headers:
            headers.update(_headers)
        return headers

    async def get(self, path, **kwargs):
        path = self._get_path(path, **kwargs)
        request = get_tornado_request(self._bastion_address, path=path)
        headers = self._get_headers(**kwargs)
        request.headers.update(headers)
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result

    async def head(self, path, **kwargs):
        path = self._get_path(path, **kwargs)
        request = get_tornado_request(path, method="HEAD")
        headers = self._get_headers(**kwargs)
        request.headers.update(headers)
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result

    async def post(self, path, **kwargs):
        path = self._get_path(path, **kwargs)
        form_data = kwargs.get("form_data", {})
        request = get_tornado_request(path, method="POST",
                                      form_urlencoded=True)
        headers = self._get_headers(**kwargs)
        request.headers.update(headers)
        request.body = urlencode(form_data)
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result
