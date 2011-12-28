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


ptah_misc
=========

`ptah_misc` is different than the other examples.  The ptah_misc is not
a Python package but a Folder full of example modules.  Each module is
an example of a specific aspect of Ptah.  The goal is to show, in isolation,
a particular feature/function of Ptah.  These are usually 1 python file.


