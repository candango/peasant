#!/usr/bin/env python
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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ec import generate_private_key


def generate_key(curve):
    """
    Generates a new Elliptic Curve private key.
    """
    return generate_private_key(curve, default_backend())
