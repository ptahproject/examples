``ptah_minicms`` README
=======================

This packages provides an example content management system (CMS).
The user experience is primitive, uses bootstrap CSS/JS and provides
a hierarchy for users to create content.  You can easily create your
own models, forms, and fields and have them show up in the system.

This example demonstrates::

- Several models: Folder, Page and File

- A set of permissions for the CMS

- Login feature

- Folder based content hierarchy

- Ability to set a Content item as the default view for a Folder

- Ability to assign a specific role to User per Content (local roles/sharing)

- Ability to define user actions (add, edit, sharing) which can be extended

``ptah_minicms`` is built solely on-top of Pyramid and Ptah.  It depends on
a number of other components, such as the ``pyramid_debugtoolbar`` only so
a developer can see how information rich the Pyramid/Ptah environment
is out-of-the-box.

Quick Start
-----------

Install into your virtualenv::

  $ /path/to/virtualenv/bin/python setup.py develop

Then start pyramid::

  $ /path/to/virtualenv/bin/pserve development.ini