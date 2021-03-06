import ptah
import ptahcms
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


@view_config(
    'sharing.html', context=ptah.ILocalRolesAware,
    permission=ptahcms.ShareContent, wrapper=ptah.wrap_layout(),
    renderer='templates/sharing.pt')

class SharingForm(ptah.form.Form):

    csrf = True

    fields = ptah.form.Fieldset(
        ptah.form.FieldFactory(
            'text',
            'term',
            title='Search term',
            description='Searches users by login and email',
            missing=''))

    users = None
    bsize = 15

    def form_content(self):
        return {'term': self.request.session.get('sharing-search-term', '')}

    def get_principal(self, id):
        return ptah.resolve(id)

    def update(self):
        super(SharingForm, self).update()

        request = self.request
        context = self.context

        self.roles = [r for r in ptah.get_roles().values() if not r.system]
        self.local_roles = local_roles = context.__local_roles__

        term = request.session.get('sharing-search-term', '')
        if term:
            self.users = list(ptah.search_principals(term))

        if 'form.buttons.save' in request.POST:
            users = []
            userdata = {}
            for attr, val in request.POST.items():
                if attr.startswith('user-'):
                    userId, roleId = attr[5:].rsplit('-',1)
                    data = userdata.setdefault(str(userId), [])
                    data.append(str(roleId))
                if attr.startswith('userid-'):
                    users.append(str(attr.split('userid-')[-1]))

            for uid in users:
                if userdata.get(uid):
                    local_roles[str(uid)] = userdata[uid]
                elif uid in local_roles:
                    del local_roles[uid]

            context.__local_roles__ = local_roles

    @ptah.form.button('Search', actype=ptah.form.AC_PRIMARY)
    def search(self):
        data, error = self.extract()

        if not data['term']:
            self.message('Please specify search term', 'warning')
            return

        self.request.session['sharing-search-term'] = data['term']
