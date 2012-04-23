""" file content implementation """
import sqlalchemy as sqla
from pyramid.view import view_config

import ptah
import ptahcms
from ptah_minicms.permissions import AddFile


class File(ptahcms.Content):
    """
    A File model that subclasses ptahcms.Content
    """

    __tablename__ = 'ptah_minicms_files'

    __type__ = ptahcms.Type(
        'file',
        title = 'File',
        description = 'A file in the site.',
        permission = AddFile,
        addview = 'addfile.html',
        )

    blobref = sqla.Column(
        sqla.Unicode,
        info = {'title': 'Data',
                'field_type': 'file',
                'uri': True})

    @ptahcms.action(permission=ptahcms.ModifyContent)
    def update(self, **data):
        """ Update file content. """
        fd = data.get('blobref')
        if fd:
            blob = ptah.resolve(self.blobref)
            if blob is None:
                blob = ptahcms.blobStorage.create(self)
                self.blobref = blob.__uri__

            blob.write(fd['fp'].read())
            blob.updateMetadata(
                filename = fd['filename'],
                mimetype = fd['mimetype'])

        self.title = data['title']
        self.description = data['description']

    @ptahcms.action(permission=ptahcms.View)
    def data(self):
        """ Download data. """
        blob = ptah.resolve(self.blobref)
        if blob is None:
            raise ptahcms.NotFound()

        return {'mimetype': blob.mimetype,
                'filename': blob.filename,
                'data': blob.read()}


@view_config('download.html', context=File, permission=ptahcms.View)
def fileDownloadView(context, request):
    data = context.data()

    response = request.response
    response.content_type = data['mimetype'].encode('utf-8')
    response.headerlist = {
        'Content-Disposition':
        'filename="%s"'%data['filename'].encode('utf-8')}
    response.body = data['data']
    return response


@view_config(
    context=File,
    permission=ptahcms.View,
    wrapper=ptah.wrap_layout(),
    renderer='ptah_minicms:templates/file.pt')
def fileView(context, request):
    return {'resolve': ptah.resolve,
            'format': ptah.format}


@view_config('addfile.html', context=ptahcms.Container, permission=AddFile)
class FileAddForm(ptahcms.AddForm):

    tinfo = File.__type__

    def chooseName(self, **kw):
        filename = kw['blobref']['filename']
        name = filename.split('\\')[-1].split('/')[-1]

        i = 1
        n = name
        while n in self.container:
            i += 1
            n = '%s-%s'%(name, i)

        return n
