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

from peasant.client.transport import (concat_url, fix_address, METHOD_POST,
                                      Transport)
from unittest import TestCase


class TransportTestCase(TestCase):

    def test_concat_url(self):
        bastion_address = fix_address("http://bastion/")
        url = concat_url(bastion_address)
        expected_url = "http://bastion"
        self.assertEqual(expected_url, url)

        bastion_address = fix_address("http://bastion/")
        url = concat_url(bastion_address, "")
        expected_url = "http://bastion"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="resource")
        expected_url = "http://bastion/resource"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="/resource")
        expected_url = "http://bastion/resource"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="resource/")
        expected_url = "http://bastion/resource/"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="/resource/")
        expected_url = "http://bastion/resource/"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="/resource",
                         query_string={})
        expected_url = "http://bastion/resource"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="/resource",
                         query_string="abc=1")
        expected_url = "http://bastion/resource?abc=1"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="/resource",
                         query_string={"abc": 1})
        expected_url = "http://bastion/resource?abc=1"
        self.assertEqual(expected_url, url)

        url = concat_url(bastion_address, path="/resource",
                         query_string={"abc": 1, "def": 2})
        expected_url = "http://bastion/resource?abc=1&def=2"
        self.assertEqual(expected_url, url)

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

    def test_kwargs_updater(self):
        transport = Transport()

        def kwargs_updater(method, **kwargs):
            kwargs['test'] = method
            return kwargs

        kwargs = {}
        transport.kwargs_updater = kwargs_updater
        kwargs = transport.update_kwargs(METHOD_POST, **kwargs)
        self.assertTrue("test" in kwargs)
        self.assertEqual(METHOD_POST, kwargs['test'])
