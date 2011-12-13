import ptah
from ptah import form

# register colorpicker assets as library
ptah.library(
    'colorpicker',
    path=('ptah_simpleauth:static/colorpicker/js/colorpicker.js',
          'ptah_simpleauth:static/colorpickerjs/eye.js',
          'ptah_simpleauth:static/colorpickerjs/utils.js'),
    type="js",
    require="jquery")

ptah.library(
    'colorpicker',
    path=('ptah_simpleauth:static/colorpicker/css/colorpicker.css',
          'ptah_simpleauth:static/colorpicker/css/layout.css',
          ),
    type='css')


@form.field('colorpicker')
class ColorPickerField(form.InputField):
    __doc__ = u'Colorpicker input widget'

    klass = u'colorpicker-widget'
    value = u''

    tmpl_input = "ptah_simpleauth:templates/colorpicker-input.pt"
    tmpl_display = "ptah_simpleauth:templates/colorpicker-display.pt"


@form.fieldpreview(ColorPickerField)
def colorpickerPreview(request):
    field = ColorPickerField(
        'ColorPickerField',
        title = 'Colorpicker field',
        description = 'Colorpicker field preview description')

    widget = field.bind('preview.', '#0000ff', {})
    widget.update(request)
    return widget.snippet('form-widget', widget)
