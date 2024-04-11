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
from peasant.client.transport_requests import RequestsTransport
from tests import chdir_fixture_app, PROJECT_ROOT
from tornado.testing import gen_test


class RequestsTransportTestCase(TornadoAsyncTestCase):
    """ Tornado based client test case. """

    def get_launcher(self) -> ProcessLauncher:
        application_dir = chdir_fixture_app("bastiontest")
        return ProcessLauncher(
            dir=application_dir, path=PROJECT_ROOT)

    def setUp(self) -> None:
        super().setUp()
        # setting tests simplefilter to ignore because requests uses a
        # keep-alive model, not closing sockets explicitly in many cases.
        # with that will cause the ResourceWarning warn be displayed in testing
        # as unittests will set warnings.simplefilter to default.
        # See:
        # - https://github.com/psf/requests/issues/3912#issuecomment-284328247
        # - https://python.readthedocs.io/en/stable/library/warnings.html#updating-code-for-new-versions-of-python
        import warnings
        warnings.simplefilter("ignore")
        self.transport = RequestsTransport(
                f"http://localhost:{self.http_port()}")

    @gen_test
    async def test_delete(self):
        expected_body = "da body"
        expected_content = b"Delete method output"
        try:
            response = self.transport.delete("/delete")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.content)

    @gen_test
    async def test_get(self):
        expected_content = b"Get method output"
        try:
            response = self.transport.get("/")
        except Exception as e:
            raise e
        self.assertEqual(expected_content, response.content)

    @gen_test
    async def test_head(self):
        expected_head_response = "Head method response"
        try:
            response = self.transport.head("/head")
        except Exception as e:
            raise e
        self.assertEqual(expected_head_response,
                         response.headers.get("head-response"))
        self.assertEqual(self.transport.user_agent,
                         response.headers.get("user-agent"))

    @gen_test
    async def test_options(self):
        expected_body = "da body"
        expected_content = b"Options method output"
        try:
            response = self.transport.options("/options")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.content)

    @gen_test
    async def test_patch(self):
        expected_body = "da body"
        expected_content = b"Patch method output"
        try:
            response = self.transport.patch("/patch", data="da body")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.content)

    @gen_test
    async def test_post(self):
        expected_body = "da body"
        expected_content = b"Post method output"
        try:
            response = self.transport.post("/post", data="da body")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.content)

    @gen_test
    async def test_put(self):
        expected_body = "da body"
        expected_content = b"Put method output"
        try:
            response = self.transport.put("/put", data="da body")
        except Exception as e:
            raise e
        self.assertEqual(expected_body, response.headers.get("request-body"))
        self.assertEqual(expected_content, response.content)
