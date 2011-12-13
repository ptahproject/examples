import transaction
from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

import ptah

# Your custom auth plugin
from ptah_simpleauth.auth import User, Session

# Import models
from ptah_simpleauth import models

auth_policy = AuthTktAuthenticationPolicy('secret')
session_factory = UnencryptedCookieSessionFactoryConfig('secret')


# WSGI Entry Point
def main(global_config, **settings):
    """ This is your application startup."""
    
    config = Configurator(settings=settings,
                          session_factory = session_factory,
                          authentication_policy = auth_policy)
    config.commit()
    config.begin()

    # init sqla engine
    import sqlahelper, sqlalchemy
    engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
    sqlahelper.add_engine(engine)
    
    # init ptah
    config.ptah_initialize()

    # create sql tables
    Base = sqlahelper.get_base()
    Base.metadata.create_all()
    transaction.commit()

    # admin user
    user = Session.query(User).first()
    if user is None:
        user = User('Admin', 'admin', 'admin@ptahproject.org', '12345')
        Session.add(user)

    # Bootstrap application data with some links; we use SQLAlchemy
    # directly so there are not application events being fired to apply owner

    links = {'sqlalchemy':'http://www.sqlalchemy.org/',
             'pyramid':'http://docs.pylonsproject.org/',
             'enfoldsystems':'http://www.enfoldsystems.com/',
             'bootstrap':'http://twitter.github.com/bootstrap/',
             'chameleon':'http://chameleon.repoze.org/',
             'sqlite':'http://www.sqlite.org/'}
             
    for name, url in links.items():
        if not Session.query(models.Link)\
               .filter(models.Link.href == url).all():
            link = models.Link(title=name,
                               href=url,
                               color='#0000ff')
            Session.add(link)

    # Need to commit links to database manually.
    transaction.commit()

    # configure ptah manage
    ptah_settings = config.ptah_get_settings(ptah.CFG_ID_PTAH)
    ptah_settings['managers'] = ['*']
    ptah_settings['disable_modules'] = [
        'rest', 'introspect', 'apps', 'permissions', 'settings']

    # we love them routes
    config.add_route('root', '/')
    config.add_route('contact-us', '/contact-us.html')
    config.add_route('edit-links', '/links/{id}/edit',
                     factory=models.factory, use_global_views=True)
    config.add_route('login', '/login.html')
    config.add_route('logout', '/logout.html')

    # static assets
    config.add_static_view('ptah201', 'ptah201:static')

    config.scan()
    return config.make_wsgi_app()
