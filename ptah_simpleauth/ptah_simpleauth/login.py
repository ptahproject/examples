from pyramid import security
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid

import ptah
from ptah import form


@view_config(route_name='login', renderer='ptah_simpleauth:templates/login.pt',
             wrapper=ptah.wrap_layout())
def login_form(request):
    login_form = form.Form(None, request)
    login_form.title = 'Login'

    login_form.fields = form.Fieldset(
        form.TextField(
            'login',
            title = u'Login Name',
            description = 'Login names are case sensitive, '\
                'make sure the caps lock key is not enabled.',
            default = u''),
        form.PasswordField(
            'password',
            title = u'Password',
            description = 'Case sensitive, make sure caps '\
                'lock is not enabled.',
            default = u''),
        )

    def loginAction(form):
        request = form.request
        data, errors = form.extract()
        if errors:
            form.message(errors, 'form-error')
            return

        info = ptah.auth_service.authenticate(data)
        if info.status:
            headers = security.remember(request, info.principal.uri)
            return HTTPFound(headers = headers, 
                             location = request.application_url)

        if info.message:
            form.message(info.message, 'warning')
            return

        form.message('You enter wrong login or password.', 'error')

    login_form.buttons.add_action('Log in', action=loginAction)
    res = login_form.update()
    if isinstance(res, HTTPFound):
        return res

    return {'rendered_login_form': login_form.render(),
            'user': ptah.resolve(authenticated_userid(request))}


@view_config(route_name='logout')
def logout_form(request):
    headers = security.forget(request)
    return HTTPFound(
        headers = headers,
        location = request.application_url)
