import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.traversal import DefaultRootFactory

import ptah
from ptah import form

# logger, check Debug Toolbar logging section or stdout
log = logging.getLogger(__name__)

@ptah.layout(name="ptah-page", context=DefaultRootFactory,
             renderer='ptah_chat:templates/layout.pt', use_global_views=True)

@ptah.layout(context=DefaultRootFactory,
             renderer='ptah_chat:templates/layout.pt', use_global_views=True)
class Layout(ptah.View):
    """ simple layout """

    links = {'sqlalchemy':'http://www.sqlalchemy.org/',
             'pyramid':'http://docs.pylonsproject.org/',
             'enfoldsystems':'http://www.enfoldsystems.com/',
             'bootstrap':'http://twitter.github.com/bootstrap/',
             'chameleon':'http://chameleon.repoze.org/',
             'sqlite':'http://www.sqlite.org/'}

    def update(self):
        self.user = ptah.auth_service.get_current_principal()
        self.isAnon = self.user is None
        self.manage_url = ptah.manage.get_manage_url(self.request)

@view_config(renderer='ptah_chat:templates/homepage.pt',
             wrapper=ptah.wrap_layout(), route_name='root')
class HomepageView(object):
    """ Homepage view """

    def __init__(self, request):
        self.request = request

    def __call__(self):
        return {'user': ptah.resolve(authenticated_userid(self.request))}
