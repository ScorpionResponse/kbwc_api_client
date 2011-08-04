from distutils.core import setup

setup(
    name = 'kbwc_api_client',
    version = '0.1.0',
    author = 'Paul Moss',
    author_email = 'mossp@oclc.org',
    packages = ['kbwc_api_client'],
    url = 'http://oclc.org/knowledgebase',
    license = 'LICENSE.txt',
    description = 'Client for the WorldCat knowledge base',
    long_description = open('README.txt').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
