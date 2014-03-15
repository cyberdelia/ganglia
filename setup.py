# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='ganglia',
    version='0.3.0',
    packages=['ganglia',],
    license='MIT',
    description="A Ganglia client",
    long_description=open('README.rst').read(),
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    test_suite='ganglia',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
)
