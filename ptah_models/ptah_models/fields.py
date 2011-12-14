import ptah


# register colorpicker assets as library
ptah.library(
    'colorpicker',
    path=('ptah_models:static/colorpicker/js/colorpicker.js',
          'ptah_models:static/colorpicker/js/eye.js',
          'ptah_models:static/colorpicker/js/utils.js'),
    type="js",
    require="jquery")

ptah.library(
    'colorpicker',
    path=('ptah_models:static/colorpicker/css/colorpicker.css',
          'ptah_models:static/colorpicker/css/layout.css'),
    type='css')


@ptah.form.field('colorpicker')
class ColorPickerField(ptah.form.InputField):
    __doc__ = u'Colorpicker input widget'

    klass = u'colorpicker-widget'
    value = u''

    tmpl_input = "ptah_models:templates/colorpicker-input.pt"
    tmpl_display = "ptah_models:templates/colorpicker-display.pt"


@ptah.form.fieldpreview(ColorPickerField)
def colorpickerPreview(request):
    field = ColorPickerField(
        'ColorPickerField',
        title = 'Colorpicker field',
        description = 'Colorpicker field preview description')

    widget = field.bind('preview.', '#0000ff', {})
    widget.update(request)
    return widget.snippet('form-widget', widget)
