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

import base64


def jose_b64(data):
    """
    Encodes data with JOSE/JWS base 64 encoding.
    """
    return base64.urlsafe_b64encode(data).decode('ascii').replace('=', '')


def to_jwk(account_key):
    """
    Creates a new request header for the specified account key.
    """
    numbers = account_key.public_key().public_numbers()
    e = numbers.e.to_bytes((numbers.e.bit_length() // 8 + 1), byteorder='big')
    n = numbers.n.to_bytes((numbers.n.bit_length() // 8 + 1), byteorder='big')
    if n[0] == 0: # for strict JWK
        n = n[1:]
    return {
        'alg': 'RS256',
        'jwk': {
            'kty': 'RSA',
            'e': jose_b64(e),
            'n': jose_b64(n),
        },
    }
