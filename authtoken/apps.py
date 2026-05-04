from django.apps import AppConfig


class AuthtokenConfig(AppConfig):
    # keep the import path correct
    name = 'authtoken'
    # app label must be unique (rest_framework.authtoken also uses 'authtoken')
    label = 'myauthtoken'
