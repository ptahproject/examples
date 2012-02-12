``ptah_chat`` README
====================

This packages provides a basic example of using pyramid_jca and pyramid_sockjs.  


Installation
------------

1. Install virtualenv::

    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    $ python2.7 ./virtualenv.py --no-site-packages pchat

2. Install cython gevent 1.0b1::

    $ ./pchat/bin/pip install cython
    $ ./pchat/bin/pip install http://gevent.googlecode.com/files/gevent-1.0b1.tar.gz

3. Install ptah & ptah_crowd:

    $ git clone git://github.com/ptahproject/ptah.git
    $ cd ptah
    $ ../pchat/bin/python setup.py develop

    $ git clone git://github.com/ptahproject/ptah_crowd.git
    $ cd ptah_crowd
    $ ../pchat/bin/python setup.py develop

3. Clone pyramid_sockjs from github and then install::

    $ git clone git://github.com/fafhrd91/pyramid_sockjs.git
    $ cd pyramid_sockjs
    $ ../pchat/bin/python setup.py develop

3. Clone pyramid_jca from github and then install::

    $ git clone git://github.com/fafhrd91/pyramid_jca.git
    $ cd pyramid_jca
    $ ../pchat/bin/python setup.py develop

4. install ptah_chat

    $ cd ptah_chat/
    $ ../pchat/bin/python setup.py develop


To run chat example use following command::

    $ cd ptah_chat/
    $ ./pchat/bin/pserve ./settings.ini


To see chat several user have to logged in.
