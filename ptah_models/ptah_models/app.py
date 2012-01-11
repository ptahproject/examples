import ptah
from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

# Import models
from ptah_models import models

auth_policy = AuthTktAuthenticationPolicy('secret')
session_factory = UnencryptedCookieSessionFactoryConfig('secret')

POPULATE_MODELS_CONTENT = 'ptah-models-content'

@ptah.populate(POPULATE_MODELS_CONTENT,
               title='Create ptah_models content',
               requires=(ptah.POPULATE_DB_SCHEMA,))
def bootstrap_data(registry):
    """ create sample content """
    
    links = {'sqlalchemy':'http://www.sqlalchemy.org/',
             'pyramid':'http://docs.pylonsproject.org/',
             'enfoldsystems':'http://www.enfoldsystems.com/',
             'bootstrap':'http://twitter.github.com/bootstrap/',
             'chameleon':'http://chameleon.repoze.org/',
             'sqlite':'http://www.sqlite.org/'}

    for name, url in links.items():
        if not ptah.get_session().query(models.Link)\
               .filter(models.Link.href == url).all():
            link = models.Link(title=name,
                               href=url,
                               color='#0000ff')
            ptah.get_session().add(link)

# WSGI Entry Point
def main(global_config, **settings):
    """ This is your application startup."""

    config = Configurator(settings=settings,
                          session_factory = session_factory,
                          authentication_policy = auth_policy)

    config.add_static_view('ptah_models', 'ptah_models:static')

    # we love them routes
    config.add_route('root', '/')
    config.add_route('contact-us', '/contact-us.html')
    config.add_route('edit-links', '/links/{id}/edit',
                     factory=models.factory, use_global_views=True)
    config.add_route('add-link', '/links/add.html')

    config.include('ptah')
    config.scan()

    # init ptah settings
    config.ptah_init_settings()

    # init sqlalchemy
    config.ptah_init_sql()

    # init ptah manage
    config.ptah_init_manage(
        managers = ['*'],
        disable_modules = ['rest', 'introspect', 'apps', 'permissions', 'settings'])

    config.commit()

    # Need to commit links to database manually.
    import transaction
    transaction.commit()

    return config.make_wsgi_app()
