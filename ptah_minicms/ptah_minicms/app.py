import transaction
from pyramid.compat import text_
from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec

import ptah
import ptah_crowd

# Your custom application permissions
from ptah_minicms.permissions import Manager

# We will add Page during bootstrap of empty AppRoot
from ptah_minicms.page import Page

# application root
from ptah_minicms.root import APP_FACTORY


def main(global_config, **settings):
    """ This is your application startup.
    """
    config = Configurator(root_factory=APP_FACTORY, settings=settings)

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
    user = Session.query(ptah_crowd.CrowdUser).first()
    if user is None:
        user = ptah_crowd.CrowdUser(
            title='Admin',
            login='admin',
            email='admin@ptahproject.org')
        user.password = ptah.pwd_tool.encode('12345')
        user.properties.validated = True
        ptah_crowd.CrowdFactory().add(user)

    # give manager role to admin
    if user.__uri__ not in root.__local_roles__:
        root.__local_roles__[user.__uri__] = [Manager.id]

    # set authcontext as admin user
    ptah.auth_service.set_userid(user.__uri__)

    # create default page
    if 'front-page' not in root.keys():
        page = Page(title='Welcome to Ptah')
        page.text = open(
            abspath_from_asset_spec('ptah_minicms:welcome.pt'), 'rb').read()

        root['front-page'] = page

    # We are not in a web request; we need to manually commit.
    transaction.commit()

    return config.make_wsgi_app()
