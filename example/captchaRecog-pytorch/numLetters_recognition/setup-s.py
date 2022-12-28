# coding: utf-8
from setuptools import setup, find_packages

# To install the library, run the following
#
# python setup-s.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

NAME = "recogcap-s"
VERSION = "1.0.0"
DESC = "This is an AI tool for captcha recognition server."
LONG_DESC = open('README.md', encoding='utf-8').read()

INSTALL_REQUIRES = [
    "flask",
    "numpy",
    "Pillow==9.3.0",
    "torch<=1.8.0"
]

setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    author_email="gaozhiyuan",
    url="https://gitee.com/openeuler/ai-tools.git",
    keywords=["AI tool", "Captcha recognition"],
    install_requires=INSTALL_REQUIRES,
    packages=['deploy_server','deploy_server.model'],
    data_files=[
        ('/root/ai-tools/recogcap/resources/weights/', ['deploy_server/resources/weights/model_weights.pth']),
        ('/usr/lib/systemd/system/', ['deploy_server/service/recogcap-s.service']),
        ('/root/ai-tools/recogcap/etc/', ['deploy_server/service/recogcap-s.sh','deploy_server/service/recogcap-s.conf']),
    ],
    entry_points={
        'console_scripts': [
            'recogcap-s=deploy_server.recogcap_server:main',
        ]
    },
    long_description=LONG_DESC,
)