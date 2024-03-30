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

from firenado.testing import TornadoAsyncTestCase
from firenado.launcher import ProcessLauncher
from peasant.client.transport import fix_address
from peasant.client.transport_tornado import (get_tornado_request,
                                              TornadoTransport)
from tests import chdir_fixture_app, PROJECT_ROOT
from tornado.testing import gen_test
from unittest import TestCase


class GetTornadoRequestTestCase(TestCase):

    def test_get_tornado_request(self):
        bastion_address = fix_address("http://bastion/")
        request = get_tornado_request(bastion_address)
        expected_url = "http://bastion"
        self.assertEqual(expected_url, request.url)

        request = get_tornado_request(bastion_address, path="resource")
        expected_url = "http://bastion/resource"
        self.assertEqual(expected_url, request.url)

        request = get_tornado_request(bastion_address, path="/resource")
        expected_url = "http://bastion/resource"
        self.assertEqual(expected_url, request.url)

        request = get_tornado_request(bastion_address, path="resource/")
        expected_url = "http://bastion/resource/"
        self.assertEqual(expected_url, request.url)

        request = get_tornado_request(bastion_address, path="/resource/")
        expected_url = "http://bastion/resource/"
        self.assertEqual(expected_url, request.url)


class TornadoTransportTestCase(TornadoAsyncTestCase):

    def get_launcher(self) -> ProcessLauncher:
        application_dir = chdir_fixture_app("bastiontest")
        return ProcessLauncher(
            dir=application_dir, path=PROJECT_ROOT)

    def setUp(self) -> None:
        super().setUp()
        self.transport = TornadoTransport(
                f"http://localhost:{self.http_port()}")

    @gen_test
    async def test_head(self):
        try:
            response = await self.transport.head("/head")
        except Exception as e:
            raise e
        self.assertEqual(response.headers.get("head-response"),
                         "Head method response")
        self.assertEqual(response.headers.get("user-agent"),
                         self.transport.user_agent)

    @gen_test
    async def test_get(self):
        try:
            response = await self.transport.get("/")
        except Exception as e:
            raise e
        self.assertEqual(response.body, b"Get method output")

    @gen_test
    async def test_post(self):
        try:
            response = await self.transport.post("/post")
        except Exception as e:
            raise e
        self.assertEqual(response.body, b"Post method output")
