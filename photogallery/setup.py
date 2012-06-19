import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'ptah',
    'pyramid',
    'pyramid_sockjs',
    'requests']

test_requires = [
    'nose',
    ]


setup(
    name='gallery',
    version='0.1',
    description='gallery',
    long_description="simple photo gallery",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
    author='Nikolay Kim',
    author_email='fafhrd91@gmail.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=test_requires,
    test_suite = 'nose.collector',
    entry_points = {
        'paste.app_factory': [
            'main = gallery.app:main']
        },
    )
