import ptah
from ptah.sockjs import handler, protocol, Protocol, Form

from .proto import AppProtocol
from .models import Gallery


@handler('addgallery', AppProtocol)
class AddGallery(Form):

    label = 'Add gallery'

    fields = ptah.form.Fieldset(
        ptah.form.TextField(
            'title',
            title = 'Title'),
        ptah.form.TextAreaField(
            'description',
            title = 'Description',
            missing = ''),
        )

    @ptah.form.button('Cancel', name='close')
    def on_cancel(self):
        pass

    @ptah.form.button('Add', name='submit', actype=ptah.form.AC_PRIMARY)
    def on_submit(self):
        data, errors = self.extract()
        if errors:
            return errors

        with ptah.sa_session() as sa:
            gallery = Gallery(user = self.protocol.user_id,
                              name = data['title'],
                              description = data['description'])
            sa.add(gallery)
            sa.flush()

            self.close()
            self.protocol.send('galleries', self.protocol.get_galleries(sa))


@handler('editgallery', AppProtocol)
class EditGallery(Form):

    label = 'Edit gallery'

    fields = ptah.form.Fieldset(
        ptah.form.TextField(
            'title',
            title = 'Title'),
        ptah.form.TextAreaField(
            'description',
            title = 'Description',
            missing = ''),
        )

    def update(self):
        # load user
        with ptah.sa_session() as sa:
            id = self.params['id']
            gallery = sa.query(Gallery).filter(Gallery.id==id).first()
            
            self.sa = sa
            self.context = gallery
            self.content = {'title': gallery.name,
                            'description': gallery.description}
            
            return super(EditGallery, self).update()

    @ptah.form.button('Cancel', name='close')
    def on_cancel(self):
        pass

    @ptah.form.button('Edit', name='submit', actype=ptah.form.AC_PRIMARY)
    def on_submit(self):
        data, errors = self.extract()
        if errors:
            return errors

        self.context.name = data['title']
        self.context.description = data['description']
        self.sa.flush()

        self.close()
        self.protocol.send('galleries', self.protocol.get_galleries(self.sa))
