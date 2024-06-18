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
from peasant.client.transport import Transport

logger = logging.getLogger(__name__)

requests_installed = False

try:
    import requests
    requests_installed = True

except ImportError:
    pass


class RequestsTransport(Transport):

    basic_headers: dict
    user_agent: str

    def __init__(self, bastion_address):
        super().__init__()
        if not requests_installed:
            logger.warn("RequestsTransport cannot be used without requests "
                        "installed.\nIt is necessary to install peasant "
                        "with extras modifiers all or requests.\n\n Ex: pip "
                        "install peasant[all] or pip install peasant[requests]"
                        "\n\nInstalling requests manually will also work.\n")
            raise NotImplementedError
        self._bastion_address = bastion_address
        self._directory = None
        self.user_agent = (f"Peasant/{get_version()} "
                           f"Requests/{requests.__version__}")
        self.basic_headers = {
            'User-Agent': self.user_agent
        }

    def get_headers(self, **kwargs):
        headers = copy.deepcopy(self.basic_headers)
        _headers = kwargs.get('headers')
        if _headers:
            headers.update(_headers)
        return headers

    def delete(self, path: str, **kwargs):
        """ Sends a delete method with basic headers.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.delete(url, **kwargs) as result:
            result.raise_for_status()
        return result

    def get(self, path, **kwargs):
        """Sends a GET request.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.get(url, **kwargs) as result:
            result.raise_for_status()
        return result

    def head(self, path, **kwargs):
        """Sends a HEAD request.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.head(url, **kwargs) as result:
            result.raise_for_status()
        return result

    def options(self, path, **kwargs):
        """Sends a OPTIONS request.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.options(url, **kwargs) as result:
            result.raise_for_status()
        return result

    def patch(self, path, **kwargs):
        """Sends a PATCH request.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.patch(url, **kwargs) as result:
            result.raise_for_status()
        return result

    def post(self, path, **kwargs):
        """Sends a POST request.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.post(url, **kwargs) as result:
            result.raise_for_status()
        return result

    def put(self, path, **kwargs):
        """Sends a PUT request.

        :param path: absolute or relative URL for the new
        :class:`requests.Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`requests.Response <Response>` object
        :rtype: requests.Response
        """
        url = self.get_url(path, **kwargs)
        headers = self.get_headers(**kwargs)
        kwargs['headers'] = headers
        with requests.put(url, **kwargs) as result:
            result.raise_for_status()
        return result
