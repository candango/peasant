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

logger = logging.getLogger(__name__)


class PeasantTransport(object):

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


try:
    from tornado.httpclient import HTTPRequest

    def get_request(url, **kwargs):
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
        print(url)
        request = HTTPRequest(url, method=method)
        if form_urlencoded:
            request.headers.add("Content-Type",
                                "application/x-www-form-urlencoded")
        return request
except ImportError:
    pass


try:
    from tornado import version as tornado_version
    from tornado.httputil import url_concat
    from tornado.httpclient import AsyncHTTPClient, HTTPClientError
    from urllib.parse import urlencode

    class TornadoTransport(PeasantTransport):

        def __init__(self, bastion_address):
            super().__init__()
            self._client = AsyncHTTPClient()
            self._bastion_address = bastion_address
            self._directory = None
            self.user_agent = (f"Peasant/{get_version()}"
                               f"Tornado/{tornado_version}")
            self._basic_headers = {
                'User-Agent': self.user_agent
            }

        async def get(self, path, **kwargs):
            headers = kwargs.get('headers')
            query_string = kwargs.get('query_string')
            if query_string:
                path = url_concat(path, query_string)
            request = get_request(self._bastion_address, path=path)
            if headers:
                request.headers.update(headers)
            return await self._client.fetch(request)

        async def head(self, path, **kwargs):
            headers = kwargs.get('headers')
            request = get_request(path, method="HEAD")
            _headers = copy.deepcopy(self._basic_headers)
            if headers:
                _headers.update(headers)
            request.headers.update(_headers)
            return await self._client.fetch(request)

        async def post(self, path, **kwargs):
            headers = kwargs.get('headers')
            form_data = kwargs.get("form_data", {})
            request = get_request(path, method="POST", form_urlencoded=True)
            _headers = copy.deepcopy(self._basic_headers)
            if headers:
                _headers.update(headers)
            request.headers.update(_headers)
            request.body = urlencode(form_data)
            try:
                result = await self._client.fetch(request)
            except HTTPClientError as error:
                result = error.response
            return result
except ImportError:
    pass
