========
Overview
========

The `examples repository <https://github.com/ptahproject/examples>`_ contains
several Python packages which demonstrate various Ptah usage.  The examples
are not released individually as packages.  You are expected to ``git clone``
this repository and work from there.

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

The `ptah_simpleauth` package demonstrates:

  * Pyramid developer toolbar
  
  * A homepage view
  
  * ``Ptah Manage`` requires authentication

Dependencies:

  * :py:mod:`ptah`

ptah_minicms
============

A miniature Content Management System (CMS) example which provides a 
sophisticated experience and demonstration of Ptah capabilities.  

This package provides:

  * Content types/models: File, Page, and Folder
  
  * Layout preview functionality
  
  * Sharing UI to assign users roles per item or folder
  
  * Homepage view
  
  * User management by using :py:mod:`ptah_crowd`
  
  * Folder operations on items: cut, copy, paste and rename.

Dependencies:

  * :py:mod:`ptah`

  * :py:mod:`ptah_crowd`


simple_forms
============

This directory contains two examples of form generation using Ptah's form
library. The idea is to show how to generate forms using the two configuration
approaches provided by the form library.

These examples do not use ``pserve`` to run.  Just use the python environment
where you have installed ptah.

Example of running one of the simple_forms examples::

  $ cd examples/simple_forms
  $ /virtualenv/bin/python form_declarative.py

form_declarative.py
~~~~~~~~~~~~~~~~~~~

Example of using :py:mod:`ptah.form` declaratively. The form example subclasses
:py:class:`ptah.form.Form` and has a validator.

  .. literalinclude:: ../simple/form_declarative.py
     :linenos:

form_imperative.py
~~~~~~~~~~~~~~~~~~

Example of using :py:mod:`ptah.form` imperatively.  The form is instantiated and
fields are added manually.  

  .. literalinclude:: ../simple/form_imperative.py
     :linenos:


simple_layout
=============

Ptah provides a :py:mod:`pyramid.renderers` independent mechanism to provide
template composition (e.g. template inheritance).  The :py:mod:`ptah_minicms`
provides an example of layout preview which draws borders around the layouts.

This is a simple example of Ptah layouts, which shows how to define layouts and
how to assign them to different parts of a site.

layout.py
~~~~~~~~~

  .. literalinclude:: ../simple/layout.py
     :linenos:
