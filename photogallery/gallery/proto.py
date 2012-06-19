import ptah
from ptah.sockjs import handler, protocol, Protocol, Form

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
            galleries.append(
                {'id': g.id,
                 'title': g.name,
                 'description': g.description})
        return {'info': galleries}

    def msg_init(self, data):
        cfg = ptah.get_settings(CFG_ID_AUTH)

        self.send('config', {'id': self.id,
                             'facebook': cfg['facebook_id'],
                             'google': cfg['google_id'],
                             'gihub': cfg['github_id']})

    def msg_list(self, data):
        if self.user_id is not None:
            with ptah.sa_session() as sa:
                self.send('galleries', self.get_galleries(sa))

    def msg_removegallery(self, data):
        if self.user_id is not None:
            with ptah.sa_session() as sa:
                sa.query(Gallery).filter(Gallery.id == data['id']).delete()
                self.send('galleries', self.get_galleries(sa))

    def msg_gallery(self, data):
        photos = []
        with ptah.sa_session() as sa:
            for photo in sa.query(Photo).filter(Photo.gallery==data['id']):
                photos.append(
                    {'id': photo.id,
                     'name': photo.name,
                     'description': photo.description,
                     'filename': photo.filename,
                     'modified': photo.modified,
                     'size': photo.size})

            g = sa.query(Gallery).filter(Gallery.id==data['id']).first()
            data = {'id': g.id,
                    'title': g.name,
                    'description': g.description,
                    'photos': photos}
            self.send('gallery', data)
