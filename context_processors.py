# Module: social_auth.context_processors
# This module is designed to expose some context processors to templates so that
# certain elements of the social authentication module can be rendered to 
# templates.  This is required for social authentication routines that require
# client side integration (such as facebook connect)
#
# Section: Version History
# 18/08/2009 (DJO) - Created File

def social(request):
    from django.conf import settings
    return { 'FACEBOOK_API_KEY': settings.FACEBOOK_API_KEY }
