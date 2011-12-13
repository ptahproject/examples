import ptah
import sqlalchemy as sqla


class Link(ptah.cms.Node):
    """ A basic model. """
    
    __tablename__ = 'ptah_simpleauth_links'
   
    # Required primary field
    __id__ = sqla.Column('id', sqla.Integer,
                         sqla.ForeignKey('ptah_nodes.id'),
                         primary_key=True)

    # Your custom fields
    title = sqla.Column(sqla.Unicode)
    href = sqla.Column(sqla.Unicode)
    color = sqla.Column(sqla.Unicode, info={'field_type': 'colorpicker'})

    # Declare it as a Ptah Model
    __type__ = ptah.cms.Type('link')


def factory(request):
    id_ = request.matchdict.get('id')
    if id_:
        return ptah.cms.Session.query(Link) \
               .filter(Link.__id__ == id_).first()

    return HTTPNotFound(location='.')
