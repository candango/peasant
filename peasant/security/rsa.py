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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import (
    generate_private_key,
)
import logging

MINIMUM_KEY_SIZE = 2048
logger = logging.getLogger(__name__)


def default_key_gen(**kwargs):
    """
    The public expoent should be always 65537.

    See: https://bit.ly/343t84g
    :param size:
    :param kwargs:
    :return:
    """
    size = kwargs.get("size", MINIMUM_KEY_SIZE)
    backend = kwargs.get("backend", default_backend)
    return generate_private_key(65537, size, backend)


def generate_key(**kwargs):
    """
    Generates a new RSA private key.
    :param size:
    :param key_gen:
    :param kwargs:
    :return:
    """
    key_gen = kwargs.get("key_gen", default_key_gen)
    return key_gen(**kwargs)
