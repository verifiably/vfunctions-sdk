#!/usr/bin/env python3

from setuptools import setup, find_packages
import os


with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A package to manage development inside nitro enclaves.'
LONG_DESCRIPTION = long_description



path_to_dependencies = os.getcwd() + "/dependencies/aws-nsm-interface/dist"

# Setting up
setup(
    name="vfunctions_sdk",
    version=VERSION,
    author="Verifiably",
    author_email="atul@verifiably.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'cbor2==5.2.0',
        'cryptography==3.2.1',
        'pycryptodome==3.9.9',
        'boto3',
        'websocket-client',
        f"aws_nsm_interface @ file://localhost/{path_to_dependencies}/aws-nsm-interface-1.0.0.tar.gz"
    ],
    python_requires='>=3.8',
    include_package_data = True,
    keywords=['python', 'nitro-enclave', 'security'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
