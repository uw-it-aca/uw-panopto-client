import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-panopto-client>`_.
"""

version_path = 'panopto_client/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='UW-Panopto-Client',
    version=VERSION,
    packages=['panopto_client'],
    include_package_data=True,
    install_requires = [
        'suds-py3~=1.4',
        'commonconf',
        'mock',
    ],
    license='Apache License, Version 2.0',
    description='An application providing access to the Panopto Video Platform SOAP API',
    long_description=README,
    url='https://github.com/uw-it-aca/uw-panopto-client',
    author = "UW-IT T&LS",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
