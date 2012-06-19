import ptah

CFG_ID_AUTH = 'auth'

ptah.register_settings(
    CFG_ID_AUTH,

    ptah.form.TextField(
        'github_id',
        title = 'Client id',
        description = 'Github client id.',
        default = ''),

    ptah.form.TextField(
        'github_secret',
        title = 'Secret',
        description = 'Github client secret.',
        default = '',
        tint = True),

    ptah.form.TextField(
        'facebook_id',
        title = 'Id',
        description = 'Facebook client id.',
        default = ''),

    ptah.form.TextField(
        'facebook_secret',
        title = 'Secret',
        description = 'Facebook client secret.',
        default = '',
        tint = True),

    ptah.form.TextField(
        'google_id',
        title = 'Id',
        description = 'Google client id.',
        default = ''),

    ptah.form.TextField(
        'google_secret',
        title = 'Secret',
        description = 'Google client secret.',
        default = '',
        tint = True),

    title = 'OAuth2 providers',
)
