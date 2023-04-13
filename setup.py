import os
from setuptools import setup, find_namespace_packages

package_version = "0.0.1"

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="hercules_protocol",
    version=package_version,
    description="Hercules protocol serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    url="https://github.com/alex-v-yakimov/hercules_protocol",
    packages=["hercules_protocol"],
    test_suite="tests",
    maintainer="Alex Yakimov",
    maintainer_email="alex_yakimov@list.ru",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
