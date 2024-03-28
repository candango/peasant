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

from .rsa import MINIMUM_KEY_SIZE
import logging

logger = logging.getLogger(__name__)


def generate_key(**kwargs):
    _type = kwargs.get("type", "rsa")

    if _type.lower() == "rsa":
        from .rsa import generate_key
        return generate_key(**kwargs)
    elif _type.lower() == "ec":
        from .ec import generate_key
        return generate_key(**kwargs)
    raise NotImplementedError


def pem_to_private_key(data):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric.ec import (
        EllipticCurvePrivateKey
    )
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
    from cryptography.hazmat.primitives.serialization import (
        load_pem_private_key
    )
    """
    Load a PEM-encoded private key.
    """
    key = load_pem_private_key(data, password=None, backend=default_backend())
    if not isinstance(key, (RSAPrivateKey, EllipticCurvePrivateKey)):
        raise NotImplementedError("Key is not a private RSA or EC key.")
    elif isinstance(key, RSAPrivateKey) and key.key_size < MINIMUM_KEY_SIZE:
        raise ValueError("The key must be %s bits or longer." %
                         MINIMUM_KEY_SIZE)
    return key


def pem_to_public_key(data):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric.ec import (
        EllipticCurvePublicKey
    )
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
    from cryptography.hazmat.primitives.serialization import (
        load_pem_public_key
    )
    """ Load a PEM-encoded public key.

    :param data:
    :return:
    """
    key = load_pem_public_key(data, backend=default_backend())
    if not isinstance(key, (RSAPublicKey, EllipticCurvePublicKey)):
        raise NotImplementedError("Key is not a public RSA or EC key.")
    elif isinstance(key, RSAPublicKey) and key.key_size < MINIMUM_KEY_SIZE:
        raise ValueError("The key must be %s bits or longer." %
                         MINIMUM_KEY_SIZE)
    return key


def key_to_pem(key):
    """
    Export a private key to PEM format.
    """
    from cryptography.hazmat.primitives.asymmetric.rsa import (
        RSAPublicKey
    )
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        PrivateFormat,
        PublicFormat,
        NoEncryption,
    )
    if hasattr(key, "private_bytes"):
        return key.private_bytes(Encoding.PEM,
                                 PrivateFormat.TraditionalOpenSSL,
                                 NoEncryption())
    elif hasattr(key, "public_bytes"):
        if isinstance(key, RSAPublicKey):
            return key.public_bytes(Encoding.PEM,
                                    PublicFormat.PKCS1)
        return key.public_bytes(Encoding.PEM,
                                PublicFormat.SubjectPublicKeyInfo)
