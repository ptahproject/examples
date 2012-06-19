import random
import ptah
from ptah.sockjs import handler, protocol, Protocol, Form
from pyramid.compat import bytes_
from pyramid.view import view_config

from .models import Gallery, Photo
from .settings import CFG_ID_AUTH


@protocol('gallery')
class AppProtocol(Protocol):

    user_id = None

    def auth(self, user):
        self.user_id = user.id
        self.user_name = user.name

        self.send('loggedin', {'id': self.user_id,
                               'name': self.user_name})

    def get_galleries(self, sa):
        galleries = []
        for g in sa.query(Gallery).filter(Gallery.user == self.user_id):
            ids = [r[0] for r in 
                   sa.query(Photo.id).filter(Photo.gallery == g.id).all()]
            if ids: 
                pid = random.choice(ids)
            else:
                pid = None

            galleries.append(
                {'id': g.id,
                 'title': g.name,
                 'description': g.description,
                 'photo': pid})
        return {'info': galleries}

    def msg_init(self, data):
        cfg = ptah.get_settings(CFG_ID_AUTH)

        self.send('config', {'id': self.id,
                             'facebook': cfg['facebook_id'],
                             'google': cfg['google_id'],
                             'gihub': cfg['github_id']})

    def msg_logout(self, data):
        self.user_id = None
        self.user_name = ''

    def msg_list(self, data):
        if self.user_id is not None:
            with ptah.sa_session() as sa:
                self.send('galleries', self.get_galleries(sa))

    def msg_removegallery(self, data):
        if self.user_id is not None:
            with ptah.sa_session() as sa:
                sa.query(Gallery).filter(Gallery.id == data['id']).delete()
                self.send('galleries', self.get_galleries(sa))

    def list_gallery(self, id, sa):
        photos = []
        for photo in sa.query(Photo).filter(Photo.gallery==id):
            photos.append(
                {'id': photo.id,
                 'name': photo.name,
                 'description': photo.description,
                 'filename': photo.filename,
                 'modified': photo.modified,
                 'size': photo.size})

        g = sa.query(Gallery).filter(Gallery.id==id).first()
        data = {'id': g.id,
                'title': g.name,
                'description': g.description,
                'photos': photos}
        return data

    def msg_gallery(self, data):
        with ptah.sa_session() as sa:
            self.send('gallery', self.list_gallery(data['id'], sa))

    def msg_upload(self, data):
        if isinstance(data['data'], unicode):
            data['data'] = data['data'].encode('latin1')

            with ptah.sa_session() as sa:
                p = Photo(gallery = data['id'],
                          name = data['filename'],
                          filename = data['filename'],
                          size = len(data['data']),
                          mimetype = data['mimetype'],
                          data = data['data'])
                sa.add(p)
                sa.flush()
                self.send('gallery', self.list_gallery(data['id'], sa))

    def msg_removephoto(self, data):
        with ptah.sa_session() as sa:
            sa.query(Photo).filter(Photo.id == data['id']).delete()
            sa.flush()
            self.send('gallery', self.list_gallery(data['id'], sa))



@view_config(route_name='view_photo')
def download(request):
    id = request.matchdict['id']

    with ptah.sa_session() as sa:
        f = sa.query(Photo).filter(Photo.id == id).first()
        if f is None:
            return HTTPNotFound()

        response = request.response

        headers = {'Content-Type': f.mimetype.encode('utf-8')}
        if f.filename:
            headers['Content-Disposition'] = \
                bytes_('filename="{0}"'.format(f.filename), 'utf-8')

        response.headers = headers
        response.body = f.data
        return response
