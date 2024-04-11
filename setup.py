#!/usr/bin/env python
#
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

import peasant
import os
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


def resolve_requires(requirements_file):
    requires = []
    if os.path.isfile(f"./{requirements_file}"):
        file_dir = os.path.dirname(f"./{requirements_file}")
        with open(f"./{requirements_file}") as f:
            for raw_line in f.readlines():
                line = raw_line.strip().replace("\n", "")
                if len(line) > 0:
                    if line.startswith("-r "):
                        partial_file = os.path.join(file_dir, line.replace(
                            "-r ", ""))
                        partial_requires = resolve_requires(partial_file)
                        requires = requires + partial_requires
                        continue
                    requires.append(line)
    return requires


setup(
    name="peasant",
    version=peasant.get_version(),
    license=peasant.__licence__,
    description="Peasant helps you to build APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/candango/peasant",
    author=peasant.get_author(),
    author_email=peasant.get_author_email(),
    extras_require={
        'all': resolve_requires("requirements/all.txt"),
        'requests': resolve_requires("requirements/requests.txt"),
        'tornado': resolve_requires("requirements/tornado.txt"),
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    packages=find_packages(),
    package_dir={'peasant': "peasant"},
    python_requires=">= 3.8",
    include_package_data=True,
    install_requires=resolve_requires("requirements/basic.txt")
)
