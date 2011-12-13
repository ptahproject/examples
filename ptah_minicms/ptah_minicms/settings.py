import ptah

ptah.register_settings(
    'ptah_minicms',

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

    ttw = True,
    title = 'ptah_minicms settings',
    description = 'Configuration settings for ptah_minicms.'
    )
