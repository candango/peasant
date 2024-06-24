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
from peasant.client.transport import (fix_address, METHOD_DELETE, METHOD_GET,
                                      METHOD_HEAD, METHOD_OPTIONS,
                                      METHOD_PATCH, METHOD_POST, METHOD_PUT,
                                      Transport)

logger = logging.getLogger(__name__)

tornado_installed = False
try:
    from tornado.httpclient import HTTPRequest
    from tornado import version as tornado_version
    from tornado.httpclient import AsyncHTTPClient
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
        method = kwargs.get("method", METHOD_GET)

        auth_username = kwargs.get("auth_username")
        auth_password = kwargs.get("auth_password")
        auth_mode = kwargs.get("auth_mode")
        connect_timeout = kwargs.get("connect_timeout")
        request_timeout = kwargs.get("request_timeout")
        if_modified_since = kwargs.get("if_modified_since")
        follow_redirects = kwargs.get("follow_redirects")
        max_redirects = kwargs.get("max_redirects")
        user_agent = kwargs.get("user_agent")
        use_gzip = kwargs.get("use_gzip")
        network_interface = kwargs.get("network_interface")
        streaming_callback = kwargs.get("streaming_callback")
        header_callback = kwargs.get("header_callback")
        prepare_curl_callback = kwargs.get("prepare_curl_callback")
        proxy_host = kwargs.get("proxy_host")
        proxy_port = kwargs.get("proxy_port")
        proxy_username = kwargs.get("proxy_username")
        proxy_password = kwargs.get("proxy_password")
        proxy_auth_mode = kwargs.get("proxy_auth_mode")
        allow_nonstandard_methods = kwargs.get("allow_nonstandard_methods")
        validate_cert = kwargs.get("validate_cert")
        ca_certs = kwargs.get("ca_certs")
        allow_ipv6 = kwargs.get("allow_ipv6")
        client_key = kwargs.get("client_key")
        client_cert = kwargs.get("client_cert")
        body_producer = kwargs.get("body_producer")
        expect_100_continue = kwargs.get("expect_100_continue")
        decompress_response = kwargs.get("decompress_response")
        ssl_options = kwargs.get("ssl_options")

        form_urlencoded = kwargs.get("form_urlencoded", False)
        request = HTTPRequest(
                url, method=method, headers=None, body=None,
                auth_username=auth_username, auth_password=auth_password,
                auth_mode=auth_mode, connect_timeout=connect_timeout,
                request_timeout=request_timeout,
                if_modified_since=if_modified_since,
                follow_redirects=follow_redirects, max_redirects=max_redirects,
                user_agent=user_agent, use_gzip=use_gzip,
                network_interface=network_interface,
                streaming_callback=streaming_callback,
                header_callback=header_callback,
                prepare_curl_callback=prepare_curl_callback,
                proxy_host=proxy_host, proxy_port=proxy_port,
                proxy_username=proxy_username, proxy_password=proxy_password,
                proxy_auth_mode=proxy_auth_mode,
                allow_nonstandard_methods=allow_nonstandard_methods,
                validate_cert=validate_cert, ca_certs=ca_certs,
                allow_ipv6=allow_ipv6, client_key=client_key,
                client_cert=client_cert, body_producer=body_producer,
                expect_100_continue=expect_100_continue,
                decompress_response=decompress_response,
                ssl_options=ssl_options,
                )
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
        self.user_agent = (f"Peasant/{get_version()} "
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

    async def delete(self, path: str, **kwargs: dict):
        """Executes a DELETE request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_DELETE
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)

    async def get(self, path: str, **kwargs: dict):
        """Executes a GET request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_GET
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)

    async def head(self, path: str, **kwargs: dict):
        """Executes a HEAD request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_HEAD
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)

    async def options(self, path: str, **kwargs: dict):
        """Executes a OPTIONS request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_OPTIONS
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)

    async def patch(self, path: str, **kwargs: dict):
        """Executes a PATCH request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_PATCH
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)

    async def post(self, path: str, **kwargs: dict):
        """Executes a POST request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_POST
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)

    async def put(self, path: str, **kwargs: dict):
        """Executes a PUT request, asynchronously returning an
        `tornado.HTTPResponse`.

        This method returns a `tornado.web.Future` whose result is an
        `tornado.web.HTTPResponse`. By default, the ``Future`` will raise an
        `tornado.web.HTTPError` if the request returned a non-200 response code
        (other errors may also be raised if the server could not be
        contacted). Instead, if ``raise_error`` is set to False, the
        response will always be returned regardless of the response
        code.
        """
        url = self.get_url(path, **kwargs)
        kwargs["method"] = METHOD_PUT
        request = get_tornado_request(url, **kwargs)
        headers = self.get_headers(**kwargs)
        request.headers.update(headers)
        kwargs = self.update_kwargs(**kwargs)
        return await self._client.fetch(request)
