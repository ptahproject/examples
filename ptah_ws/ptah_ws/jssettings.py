from pyramid.decorator import reify
from pyramid_sockjs import json
from pyramid_jca import protocol, handler, Form, Component

import ptah
from ptah.settings import ID_SETTINGS_GROUP, SettingRecord

import ptah_ws


@protocol('settings')
class SettingsComponent(Component):

    def get_info(self, name):
        group = ptah.get_cfg_storage(ID_SETTINGS_GROUP, self.registry)[name]

        schema = []
        for field in group.__fields__.values():
            if getattr(field, 'tint', False):
                value = '* * * * * * *'
            else:
                value = field.dumps(group[field.name])

            schema.append(
                ({'name': '{0}.{1}'.format(name, field.name),
                  'type': field.__class__.__name__,
                  'value': value,
                  'title': field.title,
                  'description': field.description,
                  'default': field.dumps(field.default)}))

        return {'title': group.__title__ or name,
                'description': group.__description__,
                'schema': schema,
                'name': group.__name__,
                'ttw': group.__ttw__}

    def msg_init(self, data):
        self.send('list', {'settings': {'ptah-ws':self.get_info('ptah-ws'),
                                        'ptah_crowd': self.get_info('ptah_crowd'),
                                        }})

@handler('group_edit', SettingsComponent)
class GroupEditForm(Form):

    @property
    def label(self):
        return 'Modify settings: %s'%self.title

    def form_content(self):
        return self.context

    def update(self):
        grp = ptah.get_settings(self.params['__group__'], self.request.registry)

        self.context = grp
        self.title = grp.__title__
        self.description = grp.__description__
        self.fields = grp.__fields__.omit(*grp.__ttw_skip_fields__)

        super(GroupEditForm, self).update()

    @ptah.form.button('Cancel', name='close')
    def on_cancel(self):
        pass

    @ptah.form.button('change settings', name='submit', actype=ptah.form.AC_PRIMARY)
    def modify_handler(self):
        data, errors = self.extract()
        if errors:
            self.errors = errors
            return

        with ptah_ws.get_session():
            self.context.updatedb(**data)

        self.close("Settings have been modified.")
        self.component.broadcast(
            'updated', self.component.get_info(self.context.__name__))
