import transaction
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

import ptah
from .chat import ChatProtocol

session_factory = UnencryptedCookieSessionFactoryConfig('secret')


# WSGI Entry Point
def main(global_config, **settings):
    """ This is your application startup."""

    config = Configurator(settings=settings,
                          session_factory = session_factory)

    config.ptah_init_settings()
    config.ptah_init_sql()
    config.ptah_init_manage(managers = ['*'])
    config.ptah_populate()

    # enable jca
    config.register_jca_sm()

    # internal chat
    config.register_jca_component(
        'chat', 'ptah_chat:jca/', protocol = ChatProtocol)

    # we love them routes
    config.add_route('root', '/')

    config.scan()
    return config.make_wsgi_app()
