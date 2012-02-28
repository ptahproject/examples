""" Page """
import sqlalchemy as sqla
from pyramid.view import view_config

import ptah
from ptah_ws.permissions import AddPage


class Page(ptah.cms.Content):
    """
    A Page model which subclasses ptah.cms.Content
    """

    __tablename__ = 'ptah_ws_pages'

    __type__ = ptah.cms.Type(
        'page',
        title = 'Page',
        description = 'A page in the site.',
        permission = AddPage,
        name_suffix = '.html',
        )

    text = sqla.Column(sqla.Unicode,
                       info = {'field_type': 'tinymce'})


@view_config(
    context=Page,
    permission=ptah.cms.View,
    wrapper=ptah.wrap_layout(),
    renderer='ptah_ws:templates/page.pt')
class PageView(ptah.View):
    pass
