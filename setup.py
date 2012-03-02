from setuptools import setup
from kbwc_api_client.version import __version__
import os
import sys

if sys.argv[-1] == 'test':
    os.system('python test.py')
    sys.exit()

setup(
    name = 'kbwc_api_client',
    version = __version__,
    author = 'Paul Moss',
    author_email = 'mossp@oclc.org',
    url = 'http://oclc.org/knowledgebase',
    packages = ['kbwc_api_client', 'kbwc_api_client/util',],
    install_requires = ['requests>=0.10.6'],
    license = 'Apache Software License',
    description = 'Client for the WorldCat knowledge base',
    long_description = open('README.txt').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
