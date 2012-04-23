""" Generic folder implementation """
import ptahcms
from ptah_minicms.permissions import AddFolder


class Folder(ptahcms.Container):
    """
    A Folder model which subclasses ptahcms.Container
    """

    __type__ = ptahcms.Type(
        'folder',
        title = 'Folder',
        description = 'A folder which can contain other items.',
        permission = AddFolder)
