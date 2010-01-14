# Module:   social_auth
# This module is used to define various methods by which a user can 
# login to the site using django compatible authentication for social
# sites including twitter, hyves and facebook
#
# Section: Version History
# 30/07/2009 (DJO) - Created File
# 
# Section: Configuration Instructions
# Use a syntax similar to what is outlined below to configure your 
# django settings file to provide configuration information for your
# social authentication objects
#
# SOCIAL_AUTH_CONFIG = (
#   'twitter': (
#       'button': 'tilumi/images/twitter_button_3_lo.gif',
#       'protocol': 'OAuth',
#       'consumerKey': 'l0pX3Q0sfgpG4zPQs5DGw',
#       'consumerSecret': '00tvOPob7YWu7KJCpOujd22HHOsrQlxTlqFaTRxwk',
#       'urlRequestToken': 'http://twitter.com/oauth/request_token',
#       'urlAccessToken': 'http://twitter.com/oauth/access_token',
#       'urlAuthorize': 'http://twitter.com/oauth/authorize'
#   )
#   ,'hyves': (
#   ) 
# ) # END SOCIAL_AUTH_CONFIG

DEFAULT_SOCIAL_CONFIG = {}

def getConfig():
    from django.conf import settings
    
    return getattr(settings, 'SOCIAL_AUTH_CONFIG', DEFAULT_SOCIAL_CONFIG)

def getSupportedSites():
    return getConfig().keys()
    
def persistUserSession(request, user):
    import django.contrib.auth as django_auth

    # push the current user to the request so we can retrieve it in the middleware 
    # TODO: check if this is the best way to do this... kinda doesn't feel right...
    request._social_user = user        

    # if we have a user associated with the current request, then authenticate that user
    if request.user.is_authenticated():
        # add the back end details
        # TODO: find a better way...
        for backend in django_auth.get_backends():
            request.user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
            break
        
        # log the user in
        django_auth.login(request, request.user)
