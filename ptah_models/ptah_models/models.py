import ptah
import sqlalchemy as sqla
from pyramid.httpexceptions import HTTPNotFound

@ptah.type('link')
class Link(ptah.get_base()):
    """ A basic model. """

    __tablename__ = 'links'

    # Required primary field
    __id__ = sqla.Column('id', sqla.Integer, primary_key=True)

    # Your custom fields
    title = sqla.Column(sqla.Unicode)
    href = sqla.Column(sqla.Unicode)
    color = sqla.Column(sqla.Unicode)
    #XXX , info={'field_type': 'colorpicker'})


def factory(request):
    id_ = request.matchdict.get('id')
    if id_:
        return ptah.get_session().query(Link) \
               .filter(Link.__id__ == id_).first()

    return HTTPNotFound(location='.')
