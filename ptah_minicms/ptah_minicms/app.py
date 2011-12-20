import transaction
from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec

import ptah

# Your custom application permissions
from ptah_minicms.permissions import Manager

# users
from ptah_minicms.auth import User

# We will add Page during bootstrap of empty AppRoot
from ptah_minicms.page import Page


class SiteRoot(ptah.cms.ApplicationRoot):
    """
    Application model which subclasses ptah.cms.ApplicationRoot
    """

    __type__ = ptah.cms.Type(
        'ptah_minicms-app',
        title='CMS Site Root',
        description='A root for the ptah_minicms Application')


APP_FACTORY = ptah.cms.ApplicationFactory(
    SiteRoot, '/',
    name='root', title='Ptah mini cms')


def main(global_config, **settings):
    """ This is your application startup.
    """
    config = Configurator(root_factory=APP_FACTORY, settings=settings)

    # app routes
    config.add_route('cms_login', '/login.html', use_global_views=True)
    config.add_route('cms_logout', '/logout.html', use_global_views=True)

    # static assets
    config.add_static_view('ptah_minicms', 'ptah_minicms:static')

    config.scan()

    # init sqlalchemy engine
    config.ptah_init_sql()

    # init ptah settings
    config.ptah_init_settings()

    # enable rest api
    config.ptah_init_rest()

    # enable ptah manage
    config.ptah_init_manage()

    # create sql tables
    Base = ptah.get_base()
    Base.metadata.create_all()

    # populate database
    config.commit()
    config.begin()

    # your application configuration
    ptah.auth_service.set_userid(ptah.SUPERUSER_URI)
    root = APP_FACTORY()

    # admin user
    Session = ptah.get_session()
    user = Session.query(User).first()
    if user is None:
        user = User('Admin', 'admin', 'admin@ptahproject.org', '12345')
        Session.add(user)

    # give manager role to admin
    if user.uri not in root.__local_roles__:
        root.__local_roles__[user.uri] = [Manager.id]

    # set authcontext as admin user
    ptah.auth_service.set_userid(user.uri)

    # create default page
    if 'front-page' not in root.keys():
        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            abspath_from_asset_spec('ptah_minicms:welcome.pt'), 'rb').read()

        root['front-page'] = page

    # We are not in a web request; we need to manually commit.
    transaction.commit()

    return config.make_wsgi_app()
