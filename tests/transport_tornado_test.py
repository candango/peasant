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
from peasant.client.transport_tornado import TornadoTransport
from tests import chdir_fixture_app, PROJECT_ROOT
from tornado.testing import gen_test


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
    async def test_delete(self):
        expected_body = "da body"
        expected_content = b"Delete method output"
        try:
            response = await self.transport.delete("/delete")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.body)

    @gen_test
    async def test_get(self):
        try:
            response = await self.transport.get("/")
        except Exception as e:
            raise e
        self.assertEqual(response.body, b"Get method output")

    @gen_test
    async def test_options(self):
        expected_body = "da body"
        expected_content = b"Options method output"
        try:
            response = await self.transport.options("/options")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.body)

    @gen_test
    async def test_patch(self):
        expected_body = "da body"
        expected_content = b"Patch method output"
        try:
            response = await self.transport.patch("/patch", body="da body")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.body)

    @gen_test
    async def test_post(self):
        expected_body = "da body"
        try:
            response = await self.transport.post("/post", body="da body")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(response.body, b"Post method output")

    @gen_test
    async def test_put(self):
        expected_body = "da body"
        expected_content = b"Put method output"
        try:
            response = await self.transport.put("/put", body="da body")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.body)
