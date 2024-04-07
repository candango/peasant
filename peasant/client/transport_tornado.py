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
from peasant.client.transport import concat_url, fix_address, Transport

logger = logging.getLogger(__name__)

tornado_installed = False
try:
    from tornado.httpclient import HTTPRequest
    from tornado import version as tornado_version
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
        form_urlencoded = kwargs.get("form_urlencoded", False)
        request = HTTPRequest(url, method=method)
        body = kwargs.get("body", None)
        if body:
            request.body = body
        if form_urlencoded:
            request.headers.add("Content-Type",
                                "application/x-www-form-urlencoded")
        return request
except ImportError:
    pass


class TornadoTransport(Transport):

    def __init__(self, bastion_address) -> None:
        super().__init__()
        if not tornado_installed:
            logger.warn("TornadoTransport cannot be used without tornado "
                        "installed.\nIt is necessary to install peasant "
                        "with extras modifiers all or tornado.\n\n Ex: pip "
                        "install peasant[all] or pip install peasant[tornado]"
                        "\n\nInstalling tornado manually will also work.\n")
            raise NotImplementedError
        self._client = AsyncHTTPClient()
        self._bastion_address = fix_address(bastion_address)
        self._directory = None
        self.user_agent = (f"Peasant/{get_version()}"
                           f"Tornado/{tornado_version}")
        self._basic_headers = {
            'User-Agent': self.user_agent
        }

    def get_headers(self, **kwargs):
        headers = copy.deepcopy(self._basic_headers)
        _headers = kwargs.get('headers')
        if _headers:
            headers.update(_headers)
        return headers

    async def get(self, **kwargs):
        url = concat_url(self._bastion_address, **kwargs)
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result

    async def head(self, **kwargs):
        url = concat_url(self._bastion_address, **kwargs)
        kwargs["method"] = "HEAD"
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result

    async def post(self, **kwargs):
        url = concat_url(self._bastion_address, **kwargs)
        kwargs["method"] = "POST"
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result
