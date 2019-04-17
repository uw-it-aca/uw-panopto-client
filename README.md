# UW Panopto SOAP API Client

[![Build Status](https://api.travis-ci.org/uw-it-aca/uw-panopto-client.svg?branch=master)](https://travis-ci.org/uw-it-aca/uw-panopto-client)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/uw-panopto-client/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/uw-panopto-client?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/uw-panopto-client.svg)](https://pypi.python.org/pypi/uw-panopto-client)
![Python versions](https://img.shields.io/pypi/pyversions/uw-panopto-client.svg)

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
