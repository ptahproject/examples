from pyramid import security
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import ptah
from ptah import form


@view_config(
    route_name='cms_login',
    wrapper=ptah.wrap_layout('ptah-page'),
    renderer='ptah_minicms:templates/login.pt')
def login_form(request):
    login_form = form.Form(None, request)
    login_form.title = 'Login'

    login_form.fields = form.Fieldset(
        form.TextField(
            'login',
            title = 'Login Name',
            description = 'Login names are case sensitive, '\
                'make sure the caps lock key is not enabled.',
            default = ''),
        form.PasswordField(
            'password',
            title = 'Password',
            description = 'Case sensitive, make sure caps '\
                'lock is not enabled.',
            default = ''),
        )

    def loginAction(form):
        request = form.request
        data, errors = form.extract()
        if errors:
            form.message(errors, 'form-error')
            return

        info = ptah.auth_service.authenticate(data)

        if info.status:
            headers = security.remember(request, info.principal.__uri__)
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

    return {'rendered_login_form': login_form.render()}


@view_config(route_name='cms_logout')
def logout_form(request):
    uid = ptah.auth_service.get_userid()

    if uid is not None:
        ptah.auth_service.set_userid(None)
        headers = security.forget(request)
        return HTTPFound(
            headers=headers,
            location=request.application_url)
    else:
        return HTTPFound(location=request.application_url)
