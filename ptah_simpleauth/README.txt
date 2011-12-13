``ptah_simpleauth`` README
==========================

This packages provides a basic example of using ptah.  It demonstrates::

- A homepage and a model.

- Simple form including validation. (The contact link)

- A colour picker widget for use by form and Ptah models

- Auto form generation using Ptah models

- A route view to edit Ptah models

- An authentication provider to protect the Ptah Manage UI

``ptah_simpleauth`` is built solely on-top of Pyramid.  It depends on
a number of other components, such as the ``pyramid_debugtoolbar`` so
a developer can see how information rich the Pyramid/Ptah environment
is out-of-the-box.

Quick start
-----------

Install into your virtualenv::

  $ /path/to/virtualenv/bin/python setup.py develop

Then start pyramid::

  $ /path/to/virtualenv/bin/pserve settings.ini
