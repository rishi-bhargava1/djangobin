class Preference:

    SNIPPET_EXPIRE_NEVER = 'never'
    SNIPPET_EXPIRE_1WEEK = '1 week'
    SNIPPET_EXPIRE_1MONTH = '1 month'
    SNIPPET_EXPIRE_6MONTH = '6 month'
    SNIPPET_EXPIRE_1YEAR = '1 year'

    expiration_choices = (
        (SNIPPET_EXPIRE_NEVER, 'Never'),
        (SNIPPET_EXPIRE_1WEEK, '1 week'),
        (SNIPPET_EXPIRE_1MONTH, '1 month'),
        (SNIPPET_EXPIRE_6MONTH, '6 month'),
        (SNIPPET_EXPIRE_1YEAR, '1 year'),
    )

    SNIPPET_EXPOSURE_PUBLIC = 'public'
    SNIPPET_EXPOSURE_UNLIST = 'unlisted'
    SNIPPET_EXPOSURE_PRIVATE = 'private'

    exposure_choices = (
        (SNIPPET_EXPOSURE_PUBLIC, 'Public'),
        (SNIPPET_EXPOSURE_UNLIST, 'Unlisted'),
        (SNIPPET_EXPOSURE_PRIVATE, 'Private'),
    )