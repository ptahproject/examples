""" This is an example of useing form (imperative style). """
from pprint import pprint
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import DefaultRootFactory

import ptah
from ptah import form


ptah.layout.register(
    context=DefaultRootFactory,
    renderer='__main__:templates/layout.pt')


@view_config(context=DefaultRootFactory)
def redirect(request):
    ptah.add_message(request, 'Redirect to form')
    return HTTPFound('test-form.html')


@view_config(
    'test-form.html',
    wrapper=ptah.wrap_layout(),
    context=DefaultRootFactory)
def form_view(context, request):

    myform = form.Form(context, request)

    # define fields for form
    myform.fields = form.Fieldset(

        form.TextField(
            'title',
            title = u'Title'),  # field title

        form.TextAreaField(
            'description',
            title = u'Description',
            missing = u''), # field use this value is request doesnt contain
                            # field value, effectively field is required
                            # if `missing` is not specified
        form.TextField(
            'email',
            title = u'E-Mail',
            description = u'Please provide email address.',
            validator = form.Email(), # email validator
            ),
        )

    # form actions
    def cancel_action(form):
        form.message('Cancel button', 'info')

    def update_action(form):
        data, errors = form.extract()

        if errors:
            form.message(errors, 'form-error')
            return

        pprint(data)

        form.message('Content has been updated.', 'info')
        return HTTPFound(location='.')

    myform.buttons.add_action('Update', action=update_action,
                              actype=ptah.form.AC_PRIMARY)
    myform.buttons.add_action('Cancel', action=cancel_action)

    # form default values
    myform.content = {'title': 'Test title',
                      'description': 'Context description'}

    # render form
    return myform()


if __name__ == '__main__':
    """ ...

    """
    from pyramid.config import Configurator
    from pyramid.scripts.pserve import wsgiref_server_runner
    from pyramid.session import UnencryptedCookieSessionFactoryConfig

    config = Configurator(
        settings={'sqlalchemy.url': 'sqlite://'},
        session_factory=UnencryptedCookieSessionFactoryConfig('secret'))

    config.include('ptah')
    config.scan(__name__)

    config.ptah_init_sql()

    # create sql tables
    Base = ptah.get_base()
    Base.metadata.create_all()
    config.commit()

    app = config.make_wsgi_app()
    wsgiref_server_runner(app, {})
