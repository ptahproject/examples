========
Overview
========

The `examples repository <https://github.com/ptahproject/examples>`_ contains
several Python packages which demonstrate various Ptah usage.  The examples
are not released individually as packages.  You are expected to ``git clone``
the repo and work from it.

============
Installation
============

Get the source::

  git clone git://github.com/ptahproject/examples.git

Change to the directory of the example you would like startup::

  cd examples/ptah_minicms

Then run ``/virtualenv/bin/python setup.py develop``.

Lastly startup pyramid using the .ini settings file::

  /virtualenv/bin/pserve settings.ini --reload

========
Examples
========

ptah_models
===========

The `ptah_models` package demonstrates:

  * Pyramid developer toolbar
  
  * A homepage view
  
  * ``Ptah Manage`` is accessible without authenticating
  
  * Form used for content entry of a model, ptah_models.models.Link

  * Manually constructed Form which does nothing but validates/accepts values
  
  * A example Form Field is available.  It is a colorpicker javascript widget.

Dependencies:

  * :py:mod:`ptah`


ptah_simpleauth
===============

The `ptah_simpleauth` package demonstrates::

  * Pyramid developer toolbar
  
  * A homepage view
  
  * ``Ptah Manage`` requires authentication

Dependencies:

  * :py:mod:`ptah`

ptah_minicms
============

A miniature Content Management System (CMS) example which provides a 
sophisticated experience and demonstration of Ptah capabilities.  

Dependencies:

  * :py:mod:`ptah`

  * :py:mod:`ptah_crowd`


simple
======

`simple` is different than the other examples.  The `simple` folder is not
a Python package but a collection of example modules.  Each module is
an example of a specific aspect of Ptah.  The goal is to show, in isolation,
a particular feature/function of Ptah. 

form_declarative.py
~~~~~~~~~~~~~~~~~~~

Example of using :py:mod:`ptah.form` declartively. The form example subclasses
:py:class:`ptah.form.Form` and has a validator.

form_imperative.py
~~~~~~~~~~~~~~~~~~

Example of using :py:mod:`ptah.form` imperatively.  The form is instantiated and
fields are added manually.  

layout.py
~~~~~~~~~

Ptah provides a :py:mod:`pyramid.renderer` independent mechanism to provide
template composition (e.g. template inheritance).  The :py:mod:`ptah_minicms`
provides an example of layout preview which draws borders around the layouts.


