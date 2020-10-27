# -*- coding: UTF-8 -*-
#
# Copyright 2020 Flavio Goncalves Garcia
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

import functools
import logging

logger = logging.getLogger(__name__)


class NonceServiceMixin:

    def consume(self, **kwargs):
        """ Handle a nonce sent to the request
        :param kwargs:
        :key request: The Http request being serviced.
        :key nonce: The nonce being consumed by the server.
        :return :
        """
        raise NotImplementedError

    def clear(self, **kwargs):
        """ Clears a nonce sent to the request
        :param kwargs:
        :key request: The Http request being serviced.
        :key nonce: The nonce being consumed by the server.
        """
        raise NotImplementedError

    def block_request(self, **kwargs):
        raise NotImplementedError

    def from_request(self, **kwargs):
        raise NotImplementedError

    def provided(self, **kwargs):
        raise NotImplementedError


def nonced(method):
    """ Decorates a handler to only accept requests with nonce header.
    If the request is missing the request handler we set the status as 400 with
    a malformed message.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.nonce_service.provided(request=self):
            nonce = self.nonce_service.from_request(request=self)
            if self.nonce_service.consume(
                    request=self, nonce=nonce) is not None:
                retval = method(self, *args, **kwargs)
                self.nonce_service.clear(request=self, nonce=nonce)
                return retval
        else:
            self.nonce_service.block_request(request=self)
    return wrapper
