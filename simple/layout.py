""" This is an example of layouts """
import ptah
from pyramid.compat import text_
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import DefaultRootFactory


##########################################################
###   Content hearierchy
##########################################################
class Root(object):

    __name__ = ''
    __parent__ = None
    
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        if key == 'folder1':
            folder = Folder1()
            folder.__name__ = 'folder1'
            folder.__parent__ = self
            return folder
        if key == 'folder2':
            folder = Folder2()
            folder.__name__ = 'folder2'
            folder.__parent__ = self
            return folder

        raise KeyError(key)


class Folder1(object):
    def __getitem__(self, key):
        if key == 'content':
            content = Content1()
            content.__name__ = 'content'
            content.__parent__ = self
            return content
        raise KeyError(key)


##################################
class Content1(object):
    pass

@view_config(context=Content1,
             wrapper=ptah.wrap_layout(),
             renderer='__main__:templates/layoutexample.pt')
def view(context, request):
    return {}


@ptah.layout(
    'workspace', Content1,
    parent='page',
    renderer='__main__:templates/layoutworkspace.pt')
class WorkspaceLayout(ptah.View):
    """ same as PageLayout, it uses 'page' as parent layout """

##################################

class Folder2(object):
    def __getitem__(self, key):
        if key == 'content':
            content = Content2()
            content.__name__ = 'content'
            content.__parent__ = self
            return content
        raise KeyError(key)

@ptah.layout(
    'workspace', Folder2,
    parent='workspace',
    renderer='__main__:templates/layoutfolder2-workspace.pt')
class WorkspaceLayout(ptah.View):
    """ same as PageLayout, it uses 'page' as parent layout """

####################################

class Content2(object):
    pass

@ptah.layout(
    'page', Content2,
    parent='page',
    renderer='__main__:templates/layoutcontent2-page.pt')
class PageLayout(ptah.View):
    """ same as PageLayout, it uses 'page' as parent layout """

####################################
    

@view_config(context=object,
             wrapper=ptah.wrap_layout('workspace'),
             renderer='__main__:templates/layoutexample.pt')
def view(context, request):
    return {}



##########################################################
###   Layouts
##########################################################

@ptah.layout(
    'page', Root,
    renderer='__main__:templates/layoutpage.pt')

class PageLayout(ptah.View):
    """ override 'page' layout from ptah.cmsapp

    layer - identifier, import order does matter, last imported wins
    """

    
@ptah.layout(
    'workspace', Root,
    parent='page',
    renderer='__main__:templates/layoutworkspace.pt')

class WorkspaceLayout(ptah.View):
    """ same as PageLayout, it uses 'page' as parent layout """


if __name__ == '__main__':
    """

    """
    from pyramid.config import Configurator
    from pyramid.scripts.pserve import wsgiref_server_runner
    from pyramid.session import UnencryptedCookieSessionFactoryConfig

    config = Configurator(
        settings={'sqlalchemy.url': 'sqlite://'},
        root_factory=Root,
        session_factory=UnencryptedCookieSessionFactoryConfig('secret'))

    config.include('ptah')
    config.scan(__name__)

    config.ptah_init_sql()

    # create sql tables
    Base = ptah.get_base()
    Base.metadata.create_all()
    config.commit()

    app = config.make_wsgi_app()
    wsgiref_server_runner(app, {})
