import ptah
from pyramid.view import view_config


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


@view_config(context=SiteRoot, wrapper=ptah.wrap_layout(),
             renderer='ptah_minicms:templates/homepage.pt')
class RootView(ptah.View):

    def __call__(self):
        return {'user': ptah.auth_service.get_current_principal()}
