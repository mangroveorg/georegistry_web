Georegistry Web Client -
A Reference client implementation for Georegistry Server
Georegistry is a Geospatial Health RESTful Webservice
========================================================

Written By: Alan Viars, Alex Dorey, et. al.

Copyright 2011 Columbia Univeristy / The Earth Institute

Setup Georegistry Web Client:
=============================

These instruction may need to be modified based on your flavor/version of Linux/Unix.

Setup on Ubuntu 10.10
::
    sudo apt-get install mercurlial build-essental python2.6-dev python-setuptools
    sudo easy_install pip
    git clone git://github.com/mangrove/georegistry_web.git
    cd georegistry_web
    sudo pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver