import ptah

ptah.register_settings(
    'ptah-ws',

    ptah.form.TextField(
        'band',
        default = 'Primus',
        title = 'Favorite band',
        description = 'This is your favorite band.'),

    ptah.form.TextField(
        'happy',
        default = True,
        title = 'Are you happy?',
        description = 'Does Ptah bring you happiness?'),

    ptah.form.TextAreaField(
        'field',
        default = 'Test text area',
        title = 'Favorite band 3',
        description = 'This is your favorite band.'),

    title = 'ptah_ws settings',
    description = 'Configuration settings for ptah_ws.'
    )
