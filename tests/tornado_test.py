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
from peasant.client import TornadoTransport
from tests import chdir_fixture_app, PROJECT_ROOT
from tornado.testing import gen_test


class TornadoTransportTestCase(TornadoAsyncTestCase):
    """ Tornado based client test case. """

    def get_launcher(self) -> ProcessLauncher:
        application_dir = chdir_fixture_app("bastiontest")
        return ProcessLauncher(
            dir=application_dir, path=PROJECT_ROOT)

    def setUp(self) -> None:
        super().setUp()
        self.transport = TornadoTransport(
                f"http://localhost:{self.http_port()}")

    @gen_test
    async def test_get(self):
        try:
            response = await self.transport.get("/")
        except Exception as e:
            raise e
        self.assertEqual(response.body, b"IndexHandler output")
