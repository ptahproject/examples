""" default actions """
import ptah

CATEGORY = 'cms'

ptah.uiaction(
    ptah.cms.Content,
    **{'id': 'view',
       'title': 'View',
       'action': '',
       'permission': ptah.cms.View,
       'sort_weight': 0.5,
       'category': CATEGORY})

ptah.uiaction(
    ptah.cms.Content,
    **{'id': 'edit',
       'title': 'Edit',
       'action': 'edit.html',
       'permission': ptah.cms.ModifyContent,
       'sort_weight': 0.6,
       'category': CATEGORY})

ptah.uiaction(
    ptah.cms.Container,
    **{'id': 'adding',
       'title': 'Add content',
       'action': '+/',
       'permission': ptah.cms.AddContent,
       'sort_weight': 5.0,
       'category': CATEGORY})

ptah.uiaction(
    ptah.ILocalRolesAware,
    **{'id': 'sharing',
       'title': 'Sharing',
       'action': 'sharing.html',
       'permission': ptah.cms.ShareContent,
       'sort_weight': 10.0,
       'category': CATEGORY})

"""
XXX: removed until ptah 0.3
ptah.uiaction(
    ptah.cms.Content,
    **{'id': 'layout-preview',
       'title': 'Layout preview',
       'description': 'view parameter is any registered view name for object',
       'action': 'layout-preview.html?view=',
       'permission': ptah.cms.View,
       'sort_weight': 20.0,
       'category': CATEGORY})
"""
