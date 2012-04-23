""" Page """
import sqlalchemy as sqla
from pyramid.view import view_config

import ptah
import ptahcms
from ptah_minicms.permissions import AddPage


class Page(ptahcms.Content):
    """
    A Page model which subclasses ptahcms.Content
    """

    __tablename__ = 'ptah_minicms_pages'

    __type__ = ptahcms.Type(
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
    permission=ptahcms.View,
    wrapper=ptah.wrap_layout(),
    renderer='ptah_minicms:templates/page.pt')
class PageView(ptah.View):
    pass
