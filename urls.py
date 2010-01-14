# Module: social_auth.urls
# This module defines the url patterns that are used in the for basic authentication
# operations
#
# Section: Version History
# 30/07/2009 (DJO) - Created File
#
# Section: Credits
# Based on the ragenda.auth.urls module code

import logging
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('')

LOGIN = '^%s$' % settings.LOGIN_URL.lstrip('/')
LOGOUT = '^%s$' % settings.LOGOUT_URL.lstrip('/')

# If user set a LOGOUT_REDIRECT_URL we do a redirect.
# Otherwise we display the default template.
LOGOUT_DATA = {'next_page': getattr(settings, 'LOGOUT_REDIRECT_URL', None)}

# register auth urls depending on whether we use google or hybrid auth
if 'social_auth.middleware.SocialAuthenticationMiddleware' in settings.MIDDLEWARE_CLASSES:
    urlpatterns += patterns('',
        url('^social_auth/twitter-login$', 'social_auth.views.twitter_login'),
        url('^social_auth/fb-login$', 'social_auth.views.fb_login'),
        url('^social_auth/fb-check$', 'social_auth.views.fb_check_session'),
    )
