# Module:    social_auth.middleware
# This module defines the authentication middleware to support authentication via twitter
# 
# Section: Version History
# 30/07/2009 (DJO) - Created File
#
# Section: Credits
# Based on the ragenda.auth.middleware.py

import logging

class LazySocialUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            from django.contrib.auth import get_user, login
            from django.contrib.auth.models import AnonymousUser, User

            # initialise the cached user
            request._cached_user = get_user(request)

            # if the user is anonymous, then do some twitter authentication
            if request._cached_user.is_anonymous():
                # look for the twitter user on the request
                social_user = None
                if  hasattr(request, '_social_user'):
                    social_user = request._social_user
                
                # TODO: do something to find the user here
                logging.debug("Social Middleware checking for current user - found:\n%s\n", social_user)
    
                # if the twitter user is defined, then update the cached user
                if social_user:
                    logging.debug("mapping social user to django user")
                    request._cached_user = User.get_djangouser_for_user(social_user)
                    logging.debug("updated cached user to:\n%s\n", request._cached_user)
                    
        return request._cached_user

class SocialAuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazySocialUser()
