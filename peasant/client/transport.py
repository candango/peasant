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

from __future__ import annotations

import logging
import typing as t
from urllib.parse import urlencode, urlparse

if t.TYPE_CHECKING:
    from peasant.client.protocol import Peasant

logger = logging.getLogger(__name__)

METHOD_DELETE = "DELETE"
METHOD_GET = "GET"
METHOD_HEAD = "HEAD"
METHOD_OPTIONS = "OPTIONS"
METHOD_PATCH = "PATCH"
METHOD_POST = "POST"
METHOD_PUT = "PUT"


def concat_url(url: str, path: str = None, **kwargs: dict) -> str:
    """ Concatenate a given url to a path, and query string if informed.

    :param str url: Base url
    :param str path: Path to be added to the returned url
    :param dict kwargs:
        :key path: Path to be added to the returned url
    :key query_string: Query string to be added to the returned url
    """
    query_string = kwargs.get("query_string", None)
    if query_string:
        if isinstance(query_string, dict):
            query_string = urlencode(query_string)
        if not isinstance(query_string, str):
            err = (f"'query_string' parameter should be dict, or string. "
                   f"Not {type(query_string)}")
            raise TypeError(err)
        path = f"{path}?{query_string}"
    if path is not None and path != "" and path != "/":
        if path.startswith("/"):
            path = path[1:]
        url = f"{url}/{path}"
    return url


def fix_address(address):
    parsed_address = urlparse(address)
    if parsed_address.path.endswith("/"):
        parsed_address = parsed_address._replace(path=parsed_address.path[:-1])
    return parsed_address.geturl()


class Transport:

    _kwargs_updater: t.Callable = None
    _peasant: Peasant

    @property
    def kwargs_updater(self) -> t.Callable:
        return self._kwargs_updater

    @kwargs_updater.setter
    def kwargs_updater(self, callable: t.Callable):
        self._kwargs_updater = callable

    @property
    def peasant(self) -> Peasant:
        return self._peasant

    @peasant.setter
    def peasant(self, peasant: Peasant):
        self._peasant = peasant

    def get_url(self, path: str, **kwargs: dict):
        if (path.lower().startswith("http://") or
                path.lower().startswith("https://")):
            return concat_url(path, "", **kwargs)
        return concat_url(self._bastion_address, path, **kwargs)

    def delete(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def get(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def head(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def options(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def patch(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def post(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def post_as_get(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def put(self, path: str, **kwargs: dict):
        raise NotImplementedError

    def set_directory(self):
        raise NotImplementedError

    def new_nonce(self):
        raise NotImplementedError

    def is_registered(self):
        raise NotImplementedError

    def update_kwargs(self, method, **kwargs):
        if self.kwargs_updater is None:
            return kwargs
        return self.kwargs_updater(method, **kwargs)
