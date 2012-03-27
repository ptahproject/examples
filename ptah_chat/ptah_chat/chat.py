""" internal chat """
import ptah
from datetime import datetime
from pyramid_jca import Protocol


class ChatProtocol(Protocol):

    def __init__(self, *args, **kw):
        super(ChatProtocol, self).__init__(*args, **kw)

        principal = ptah.auth_service.get_current_principal()
        self.user_id = principal.__uri__.replace(':','_')
        self.user_name = principal.name

    def on_closed(self):
        super(ChatProtocol, self).on_closed()

        found = False
        for user in self.instances.values():
            if user.user_id == self.user_id:
                found = True
                break

        if not found:
            self.broadcast('disconnected', {'uid': self.user_id})

    def msg_init(self, data):
        """ init message handler """
        users = []
        for user in self.instances.values():
            if user.user_id != self.user_id:
                users.append({'uid': user.user_id, 'name': user.user_name})

        info = {'uid': self.user_id,
                'name': self.user_name,
                'users': users}
        self.send('list', info, tmpl='chat.user')

        msg = {'uid': self.user_id,
               'name': self.user_name}
        self.broadcast('joined', msg, tmpl='chat.user')

    def msg_message(self, data):
        """ 'message' message handler """
        msg = {'uid': self.user_id,
               'name': self.user_name,
               'date': datetime.utcnow(),
               'message': data['message']}

        for user in self.instances.values():
            if user.user_id == data['uid']:
                user.send('message', msg)
