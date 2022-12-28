# coding: utf-8
from setuptools import setup, find_packages

# To install the library, run the following
#
# python setup-c.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

NAME = "recogcap-c"
VERSION = "1.0.0"
DESC = "This is an AI tool for captcha recognition client."
LONG_DESC = open('README.md', encoding='utf-8').read()

INSTALL_REQUIRES = [
    "requests",
    "captcha",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    author_email="gaozhiyuan",
    url="https://gitee.com/openeuler/ai-tools.git",
    keywords=["AI tool", "Captcha recognition"],
    install_requires=INSTALL_REQUIRES,
    packages=['deploy_client'],
    entry_points={
        'console_scripts': [
            'recogcap-c=deploy_client.recogcap_client:main',
        ]
    },
    long_description=LONG_DESC,
)