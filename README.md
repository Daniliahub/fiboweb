=======
fiboweb
=======

Live project
============

URL: http://fiboweb-developmet.rhcloud.com/

Setup
=====

Create a virtual environment using:

```
$ virtualenv virt --no-site-packages
```

Activate the virtual environment using
```
source virt/bin/activate
```

Install the packages required for this project to run:

```
pip install -r requirements.txt
```

Note: Redis should be installed and running on localhost:6379

Run
===

Do these once:

```
$ ./manage.py staticcollect
```

```
$ ./manage.py migrate
```

Now start the server:
```
$ ./manage.py runserver
```

Description
===========

Important parts of this project to look at:

1. `fiboweb.web.utils.NthFibonacci` is the Fibonacci number generator.
2. `fiboweb.web.middleware.ProcessTimeMiddleware` is the django view process time calculator.


Run the tests
=============
```
$ ./manage.py test
```
