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

from cartola.config import get_from_string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec


def default_key_gen(**kwargs):
    curve = kwargs.get("curve", ec.SECP384R1)
    backend = kwargs.get("backend", default_backend)
    return ec.generate_private_key(curve=curve, backend=backend)


def generate_key(**kwargs):
    """
    Generates a new Elliptic Curve private key.
    """
    key_gen = kwargs.get("key_gen", default_key_gen)
    if isinstance(key_gen, str):
        key_gen = get_from_string(key_gen)
    return key_gen()
