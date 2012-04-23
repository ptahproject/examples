""" app permissions and roles """
import ptah
import ptahcms

AddPage = ptah.Permission('ptah_minicms: Add page', 'Add page')
AddFile = ptah.Permission('ptah_minicms: Add file', 'Add file')
AddFolder = ptah.Permission('ptah_minicms: Add folder', 'Add folder')

ptah.Everyone.allow(ptahcms.View)
ptah.Authenticated.allow(ptahcms.AddContent)

Viewer = ptah.Role('viewer', 'Viewer')
Viewer.allow(ptahcms.View)

Editor = ptah.Role('editor', 'Editor')
Editor.allow(ptahcms.View, ptahcms.ModifyContent)

Manager = ptah.Role('manager', 'Manager')
Manager.allow(ptahcms.ALL_PERMISSIONS)

ptah.Owner.allow(ptahcms.DeleteContent)
