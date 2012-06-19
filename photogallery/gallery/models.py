import ptah
import sqlalchemy as sqla
from datetime import datetime


class Gallery(ptah.get_base()):

    __tablename__ = 'gallery'

    id = sqla.Column(sqla.Integer, primary_key=True)
    user = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'))
    name = sqla.Column(sqla.Unicode(255))
    description = sqla.Column(sqla.UnicodeText())


class Photo(ptah.get_base()):

    __tablename__ = 'photos'

    id = sqla.Column(sqla.Integer, primary_key=True)
    gallery = sqla.Column(sqla.Integer, sqla.ForeignKey('gallery.id'))
    name = sqla.Column(sqla.Unicode(255))
    description = sqla.Column(sqla.UnicodeText())
    filename = sqla.Column(sqla.Unicode(255))
    mimetype = sqla.Column(sqla.String(20))
    created = sqla.Column(sqla.DateTime())
    modified = sqla.Column(sqla.DateTime())
    size = sqla.Column(sqla.Integer())
    data = sqla.orm.deferred(sqla.Column(sqla.LargeBinary))

    def __init__(self, **kw):
        self.created = datetime.utcnow()
        self.modified = datetime.utcnow()

        super(Photo, self).__init__(**kw)
