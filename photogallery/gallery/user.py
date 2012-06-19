import ptah
import sqlalchemy as sqla
from datetime import datetime


@ptah.type('user', 'User')

class User(ptah.get_base()):
    """Default user
    
    ``name``: User name.

    ``email``: User email.

    ``properties``: User properties.
    """

    __tablename__ = 'users'

    id = sqla.Column(sqla.Integer, primary_key=True)
    token = sqla.Column(sqla.String(255), index=True)
    source = sqla.Column(sqla.String(18))
    name = sqla.Column(sqla.Unicode(255))
    email = sqla.Column(sqla.Unicode(255), unique=True)
    joined = sqla.Column(sqla.DateTime())
    properties = sqla.Column(ptah.JsonDictType(), default={})

    def __init__(self, **kw):
        self.joined = datetime.utcnow()
        self.properties = {}

        super(User, self).__init__(**kw)

    def __str__(self):
        return self.name

    def __name__(self):
        return str(self.id)

    def __repr__(self):
        return '%s<%s:%s>'%(self.__class__.__name__, self.name, self.__uri__)

    _sql_get_id = ptah.QueryFreezer(
        lambda: ptah.get_session().query(User)\
            .filter(User.id==sqla.sql.bindparam('id')))

    @classmethod
    def get_byid(cls, id):
        return cls._sql_get_id.first(id=id)

    _sql_get_token = ptah.QueryFreezer(
        lambda: ptah.get_session().query(User)\
            .filter(User.token==sqla.sql.bindparam('token')))

    @classmethod
    def get_bytoken(cls, token):
        return cls._sql_get_token.first(token=token)


@ptah.auth_provider('auth')
class AuthProvider(object):

    _sql_get_login = ptah.QueryFreezer(
        lambda: ptah.get_session().query(User)\
            .filter(User.login==sqla.sql.bindparam('login')))

    _sql_search = ptah.QueryFreezer(
        lambda: ptah.get_session().query(User) \
            .filter(sqla.sql.or_(
                User.name.contains(sqla.sql.bindparam('term')),
                User.email.contains(sqla.sql.bindparam('term'))))\
            .order_by(sqla.sql.asc('name')))

    def authenticate(self, creds):
        login, password = creds['login'], creds['password']

        user = self._sql_get_login.first(login=login)
        if user is not None:
            if ptah.pwd_tool.check(user.password, password):
                return user

    def get_principal_bylogin(self, login):
        return self._sql_get_login.first(login=login)

    def add(self, user):
        """ Add user to crowd application. """
        Session = ptah.get_session()
        Session.add(user)
        Session.flush()

        return user

    def get_user_bylogin(self, login):
        """ Given a login string return a user """
        return self._sql_get_login.first(login=login)
