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
import typing
from urllib.parse import urlparse

if typing.TYPE_CHECKING:
    from peasant.client.protocol import Peasant

logger = logging.getLogger(__name__)


def fix_address(address):
    parsed_address = urlparse(address)
    if parsed_address.path.endswith("/"):
        parsed_address = parsed_address._replace(path=parsed_address.path[:-1])
    return parsed_address.geturl()


class Transport:

    _peasant: Peasant

    @property
    def peasant(self) -> Peasant:
        return self._peasant

    @peasant.setter
    def peasant(self, peasant: Peasant):
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
