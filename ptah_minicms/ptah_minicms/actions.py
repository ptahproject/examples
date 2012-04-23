""" default actions """
import ptah
import ptahcms

CATEGORY = 'cms'

ptah.uiaction(
    ptahcms.Content,
    **{'id': 'view',
       'title': 'View',
       'action': '',
       'permission': ptahcms.View,
       'sort_weight': 0.5,
       'category': CATEGORY})

ptah.uiaction(
    ptahcms.Content,
    **{'id': 'edit',
       'title': 'Edit',
       'action': 'edit.html',
       'permission': ptahcms.ModifyContent,
       'sort_weight': 0.6,
       'category': CATEGORY})

ptah.uiaction(
    ptahcms.Container,
    **{'id': 'adding',
       'title': 'Add content',
       'action': '+/',
       'permission': ptahcms.AddContent,
       'sort_weight': 5.0,
       'category': CATEGORY})

ptah.uiaction(
    ptahcms.Container,
    **{'id': 'listing',
       'title': 'Folder listing',
       'action': 'listing.html',
       'permission': ptahcms.View,
       'sort_weight': 6.0,
       'category': CATEGORY})

ptah.uiaction(
    ptah.ILocalRolesAware,
    **{'id': 'sharing',
       'title': 'Sharing',
       'action': 'sharing.html',
       'permission': ptahcms.ShareContent,
       'sort_weight': 10.0,
       'category': CATEGORY})

ptah.uiaction(
    ptahcms.Content,
    **{'id': 'layout-preview',
       'title': 'Layout preview',
       'description': 'view parameter is any registered view name for object',
       'action': 'layout-preview.html?view=',
       'permission': ptahcms.View,
       'sort_weight': 20.0,
       'category': CATEGORY})
