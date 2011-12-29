import transaction
from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

import ptah

# Your custom auth plugin
from ptah_simpleauth.auth import User

auth_policy = AuthTktAuthenticationPolicy('secret')
session_factory = UnencryptedCookieSessionFactoryConfig('secret')


# WSGI Entry Point
def main(global_config, **settings):
    """ This is your application startup."""

    config = Configurator(settings=settings,
                          session_factory = session_factory,
                          authentication_policy = auth_policy)

    # init ptah settings
    config.ptah_init_settings()

    # init sqlalchemy engine
    config.ptah_init_sql()

    # configure ptah manage
    config.ptah_init_manage(
        managers = ['*'],
        disable_modules = ['rest', 'introspect', 'apps', 'permissions'])

    # we love them routes
    config.add_route('root', '/')
    config.add_route('login', '/login.html')
    config.add_route('logout', '/logout.html')

    # static assets
    config.add_static_view('ptah_simpleauth', 'ptah_simpleauth:static')

    config.scan()

    # create sql tables
    Base = ptah.get_base()
    Base.metadata.create_all()
    transaction.commit()

    # populate database
    config.commit()
    config.begin()

    Session = ptah.get_session()

    # admin user
    user = Session.query(User).first()
    if user is None:
        user = User('Admin', 'admin', 'admin@ptahproject.org', '12345')
        Session.add(user)

    transaction.commit()

    return config.make_wsgi_app()
