import os
from setuptools import setup, find_packages

requires = [
    'gevent >= 1.0b1',
    'ptah>=0.4.0dev',
    'ptah_crowd',
    'pyramid_jca',
    'pyramid_sockjs',
    'pyramid>1.3a6',
    'pyramid_debugtoolbar']

setup(name='ptah_chat',
      version='0.1',
      description='ptah async chat',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points = """\
        [paste.app_factory]
        main = ptah_chat.app:main
      """,
      )
