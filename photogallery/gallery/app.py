import ptah
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from .facebook import facebook_process


def main(global_config, **settings):
    """ Function which returns a configured Pyramid/Ptah WSIG Application """
    config = Configurator(
        settings=settings,
        session_factory=UnencryptedCookieSessionFactoryConfig('secret'))

    # Info: This includes packages which have Pyramid configuration
    config.include('ptah')
    config.include('pyramid_sockjs')

    # ptah init
    config.ptah_init_sql()
    config.ptah_init_settings()
    config.ptah_init_sockjs()
    config.ptah_populate()
    config.ptah_init_manage(managers='*')

    # static assets
    config.add_static_view('_gallery', 'gallery:static')

    # amd
    config.register_amd_module('gallery', 'gallery:static/app.js')

    # mustache
    config.register_mustache_bundle('gallery-tmpls', 'gallery:templates')

    # facebook
    config.add_route("facebook_process", "/_facebook_auth",
                     use_global_views=True)
    config.add_view(route_name='facebook_process', view=facebook_process)

    # view photo
    config.add_route('view_photo', pattern='/_photos/{id}')

    # app route
    config.add_route('root', '/')
    config.add_view(route_name='root', renderer='gallery:app.pt')

    config.scan()
    return config.make_wsgi_app()


import ptah
ptah.library(
    'gallery',
    path='gallery:static/styles.css',
    type="css",
    require=('bootstrap',))
