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

from importlib import reload
import os

TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
FIXTURES_ROOT = os.path.join(TEST_ROOT, "fixtures")
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_ROOT, ".."))


def chdir_fixture_app(app_name, **kwargs):
    dir_name = kwargs.get("dir_name", None)
    suppress_log = kwargs.get("suppress_log", False)
    fixture_root = kwargs.get("fixture_root", "fixtures")
    test_app_dirname = os.path.join(TEST_ROOT, fixture_root, app_name)
    if dir_name is not None:
        test_app_dirname = os.path.join(TEST_ROOT, fixture_root,
                                        dir_name, app_name)
    os.chdir(test_app_dirname)
    if suppress_log:
        import logging
        for handler in logging.root.handlers[:]:
            # clearing loggers, solution from: https://bit.ly/2yTchyx
            logging.root.removeHandler(handler)
    return test_app_dirname


def chdir_app(app_name, directory=None):
    """ Change to the application directory located at the resource directory
    for conf tests.

    The conf resources directory is firenado/tests/resources/conf.

    :param app_name: The application name
    :param directory: The directory to be changed
    """
    import firenado.conf

    test_dirname, filename = os.path.split(os.path.abspath(__file__))
    if directory:
        test_app_dirname = os.path.join(test_dirname, 'resources',
                                        directory, app_name)
    else:
        test_app_dirname = os.path.join(test_dirname, 'resources', app_name)
    os.chdir(test_app_dirname)
    reload(firenado.conf)
