import os
from setuptools import setup, find_packages


def readme(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as file:
        return file.read()


setup(
    name="ua_box_api",
    version="1.0.0",
    packages=find_packages(),
    author="Ryan Johannes-Bland",
    author_email="rjjohannesbland@email.arizona.edu",
    description=(
        "Provides easy interface for making REST requests to University of "
        "Arizona Box file storage."
    ),
    long_description=readme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/UACoreFacilitiesIT/UA-Box-API",
    license="MIT",
    install_requires=["boxsdk"],
)
