import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.traversal import DefaultRootFactory

import ptah
from ptah import form

from ptah_simpleauth import models

# logger, check Debug Toolbar logging section or stdout
log = logging.getLogger(__name__)


@ptah.layout(context=models.Link,
             renderer='ptah_simpleauth:templates/layout.pt', use_global_views=True)
@ptah.layout(context=DefaultRootFactory,
             renderer='ptah_simpleauth:templates/layout.pt', use_global_views=True)
class Layout(ptah.View):
    """ simple layout """

    def update(self):
        self.user = ptah.auth_service.get_current_principal()
        self.isAnon = self.user is None
        self.manage_url = ptah.manage.get_manage_url(self.request)

        # query for links to populate links box
        self.links = ptah.Session.query(models.Link)


class Telephone(form.Regex):
    """ An example validator.  See ptah.form.validators for more info."""
    
    def __init__(self, msg=None):
        log.info('Constructing a Telephone field validator')
        if msg is None:
            msg = "Invalid telephone number"
        super(Telephone, self).__init__(
            u'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$', msg=msg)


# This is a "class view", you do not need to use a class for your 
# view. You can use a Function view as provided below.

@view_config(renderer='ptah_simpleauth:templates/homepage.pt',
             wrapper=ptah.wrap_layout(), route_name='root')
class HomepageView(object):
    """ Homepage view """

    def __init__(self, request):
        self.request = request

    def __call__(self):
        return {'user': ptah.resolve(authenticated_userid(self.request))}


# This is a "function view", you do not need to use a function for your 
# view.  You can use a Class view as provided above.

@view_config(wrapper=ptah.wrap_layout(), route_name='contact-us')
def contact_us(context, request):
    contactform = form.Form(context, request)
    contactform.label = 'Contact us'

    contactform.fields = form.Fieldset(

        form.TextField(
            'fullname',
            title = u'First & Last Name'),  

        form.TextField(
            'phone',
            title = u'Telephone number',
            description=u'Please provide telephone number',
            validator = Telephone()),

        form.TextField(
            'email',
            title = u'Your email',
            description = u'Please provide email address.',
            validator = form.Email()),

        form.TextAreaField(
            'subject',
            title = u'How can we help?',
            missing = u''), # field use this value is request doesnt contain
                            # field value, effectively field is required
                            # if `missing` is not specified
        )

    # form actions
    def cancelAction(form):
        return HTTPFound(location='/')

    def updateAction(form):
        data, errors = form.extract()

        if errors:
            form.message(errors, 'form-error')
            return

        # form.context is ...
        form.context.fullname = data['fullname']
        form.context.phone = data['phone']
        form.context.email = data['email']
        form.context.subject = data['subject']

        # You would add any logic/database updates/insert here.
        # You would probably also redirect.
       
        log.info('The form was updated successfully')
        form.message('The form was updated successfully')

    contactform.buttons.add_action(
        'Contact us', action=updateAction, actype=form.AC_PRIMARY)
    contactform.buttons.add_action(
        'Cancel', action=cancelAction)

    # form default values
    contactform.content = {}

    return contactform()


@view_config(context=models.Link,
             wrapper=ptah.wrap_layout(),
             route_name='edit-links')
def edit_link(context, request):
    linkform = form.Form(context,request)
    linkform.fields = models.Link.__type__.fieldset
    linkform.label = 'Edit link'

    def cancelAction(form):
        return HTTPFound(location='/')

    def updateAction(form):
        data, errors = form.extract()
        if errors:
            return
        form.context.title = data['title']
        form.context.href = data['href']
        form.context.color = data['color']

    linkform.buttons.add_action('Update', action=updateAction)
    linkform.buttons.add_action('Back', action=cancelAction)
    linkform.content = {'title':context.title,
                        'href':context.href,
                        'color':context.color}

    return linkform()
