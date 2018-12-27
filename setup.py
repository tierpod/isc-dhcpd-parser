#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name="isc-dhcpd-parser",
    version="0.1",
    description="Parser for isc-dhcp config files (dhcpd.conf)",
    author="Pavel Podkorytov",
    author_email="pod.pavel@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    scripts=["bin/isc_dhcpd_leases.py"],
    install_requires=["ply"],
)
