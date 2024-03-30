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

from peasant.client.transport import fix_address
from unittest import TestCase


class TransportTestCase(TestCase):

    def test_fix_address(self):
        address = "http://localhost"
        expected_address = "http://localhost"
        fixed_address = fix_address(address)
        self.assertEqual(expected_address, fixed_address)

        address = "https://localhost/"
        expected_address = "https://localhost"
        fixed_address = fix_address(address)
        self.assertEqual(expected_address, fixed_address)

        address = "http://localhost/a/path/"
        expected_address = "http://localhost/a/path"
        fixed_address = fix_address(address)
        self.assertEqual(expected_address, fixed_address)
