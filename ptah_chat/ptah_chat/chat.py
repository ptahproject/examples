""" internal chat """
import ptah
from datetime import datetime
from pyramid_jca import Session
from pyramid_sockjs import SessionManager


class Session(Session):

    def __init__(self, *args, **kw):
        super(Session, self).__init__(*args, **kw)

        principal = ptah.auth_service.get_current_principal()
        self.user_id = principal.__uri__.replace(':','_')
        self.user_name = principal.name

    def on_closed(self):
        self.manager.unassign(self)

        found = False
        for uid, user in self.manager.list_users():
            if uid == self.user_id:
                found = True
                break

        if not found:
            for uid, user in self.manager.list_users():
                user.send('disconnected', {'uid': self.user_id})

    def msg_init(self, data):
        """ init message handler """
        self.manager.assign(self)

        users = []
        for uid, user in self.manager.list_users():
            if uid != self.user_id:
                users.append({'uid': uid, 'name': user.user_name})

        info = {'uid': self.user_id,
                'name': self.user_name,
                'users': users}
        self.send('list', info, tmpl='chat.user')

        msg = {'uid': self.user_id,
               'name': self.user_name}
        self.manager.broadcast('joined', msg, tmpl='chat.user')

    def msg_message(self, data):
        """ 'message' message handler """
        msg = {'uid': self.user_id,
               'name': self.user_name,
               'date': datetime.utcnow(),
               'message': data['message']}

        for user in self.manager.get_user(data['uid']):
            user.send('message', msg)


class ChatSessionManager(SessionManager):

    factory = Session

    def __init__(self, name, registry, **kw):
        super(ChatSessionManager, self).__init__(name, registry, **kw)

        self.users = {}

    def assign(self, session):
        data = self.users.setdefault(session.user_id, [])
        data.append(session)

    def unassign(self, session):
        data = self.users.get(session.user_id)
        if data and session in data:
            data.remove(session)
            if not data:
                del self.users[session.user_id]

    def get_user(self, uid):
        return self.users.get(uid)

    def list_users(self):
        for uid, data in self.users.items():
            yield uid, data[0]
