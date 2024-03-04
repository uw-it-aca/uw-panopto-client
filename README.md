# UW Panopto SOAP API Client

[![Build Status](https://github.com/uw-it-aca/uw-panopto-client/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/uw-panopto-client/actions)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/uw-panopto-client/badge.svg?branch=main)](https://coveralls.io/r/uw-it-aca/uw-panopto-client?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/uw-panopto-client.svg)](https://pypi.python.org/pypi/uw-panopto-client)
![Python versions](https://img.shields.io/badge/python-3.10-blue.svg)

An application providing access to the Panopto Video Platform SOAP API

Installation
------------

**Project directory**

Install uw-panopto-client in your project.

    $ cd [project]
    $ pip install UW-Panopto-Client

Project settings.py
------------------

**Panopto API settings**

    PANOPTO_API_USER = '<user context for API calls>'
    PANOPTO_API_APP_ID = '<Application context ID>'
    PANOPTO_API_TOKEN = '<Panopto GUID>'
    PANOPTO_SERVER = '<Panopto Server Name>'
