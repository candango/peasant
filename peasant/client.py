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

import logging

logger = logging.getLogger(__name__)


class PeasantTransport(object):

    _peasant: 'Peasant'

    def __init__(self):
        self._peasant = None

    @property
    def peasant(self):
        return self._peasant

    @peasant.setter
    def peasant(self, peasant):
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
