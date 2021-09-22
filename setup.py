#!/usr/bin/env python
#
# Copyright 2020 Flavio Garcia
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
from codecs import open
from setuptools import find_packages, setup
import sys

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    print("error: Upgrade to a pip version newer than 10. Run \"pip install "
          "--upgrade pip\".")
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()


# Solution from http://bit.ly/29Yl8VN
def resolve_requires(requirements_file):
    try:
        requirements = parse_requirements("./%s" % requirements_file,
                                          session=False)
        return [str(ir.req) for ir in requirements]
    except AttributeError:
        # for pip >= 20.1.x
        # Need to run again as the first run was ruined by the exception
        requirements = parse_requirements("./%s" % requirements_file,
                                          session=False)
        # pr stands for parsed_requirement
        return [str(pr.requirement) for pr in requirements]


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
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    packages=find_packages(),
    package_dir={'peasant': "peasant"},
    include_package_data=True,
    install_requires=resolve_requires("requirements/basic.txt")
)
