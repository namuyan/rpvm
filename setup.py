#!/user/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

try:
    readme = open('README.md', mode='r').read()
except Exception:
    readme = ''

try:
    install_requires = open('requirements.txt', mode='r').read()
except Exception:
    install_requires = None


setup(
    name="rpvm",
    version='0.1.0a1',
    url='https://github.com/namuyan/rpvm',
    author='namuyan',
    description='Restricted Python Virtual Machine',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=install_requires,
    license="MIT Licence",
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
