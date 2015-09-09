ACA Panopto SOAP API Client
===========================

A django application providing access to the Panopto Video Platform SOAP API

Installation
------------

**Project directory**

Install django-panopto-client in your project.

    $ cd [project]
    $ pip install -e git+https://github.com/uw-it-aca/django-panopto-client/#egg=django_panopto_client

Project settings.py
------------------

**Panopto API settings**

    PANOPTO_API_USER = '<user context for API calls>'
    PANOPTO_API_APP_ID = '<Application context ID>'
    PANOPTO_API_TOKEN = '<Panopto GUID>'
    PANOPTO_SERVER = '<Panopto Server Name>'
