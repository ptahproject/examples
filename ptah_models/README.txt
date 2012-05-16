``ptah_models`` README
==========================

This packages provides a basic example of using ptah.  It demonstrates::

- A homepage and a model.

- Simple form including validation. (The contact link)

- A colour picker widget for use by form and Ptah models

- Auto form generation using Ptah models

- A route view to edit Ptah models

``ptah_models`` is built solely on-top of Pyramid & Ptah.  It depends on
a number of other components, such as the ``pyramid_debugtoolbar`` so
a developer can see how information rich the Pyramid/Ptah environment
is out-of-the-box.

Quick start
-----------

Activate virtualenv on nix::

  $ source /path/to/virtualenv/bin/activate
  
Activate virtualenv r on Windows:

  c:\path\to\virtualenv\scripts\activate.exe

Change to the ptah_models directory.

Install the `ptah_models` package into python::

  $ (virtualenv) python setup.py develop

Run the schema generation::

  $ (virtualenv) ptah-populate settings.ini -a

Then start pyramid::

  $ (virtualenv) pserve settings.ini
