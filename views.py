# Module:   twitter_auth.views
# This module is used to define the views that are appropriate in the twitter authentication 
# django application
#
# Section: Version History
# 08/06/2009 (DJO) - Created File

import logging
import social_auth
from gaetools import twitter
from django.http import HttpResponse, Http404, HttpResponseRedirect
from ragendja.template import render_to_response
from django.contrib.auth.models import User
import django.contrib.auth.views as django_views

def login_required(request):
    """
    This view simply informs the user that they need to login to get access to the system.  I believe this is polite
    rather than taking the user straight to twitter when they need to login we at least give them the option of not
    doing so first.
    """
    
    # return to the home page
    return render_to_response(request, 'social_auth/login_required.html')    

def twitter_login(request):
    """
    The login request is defined to handle the Twitter authentication login view
    """
    
    # initialise the oauth_request_token
    oauth_request_token = None
    if 'oauth_token' in request.GET:
        oauth_request_token = request.GET['oauth_token']
    
    try:
        # create the new twitter verify request
        verifyReq = twitter.TwitterLoginRequest(True, oauth_request_token)
        
        # execute the request
        verifyReq.execute()
        
        # if the verification was successful, we will have a valid twitter id
        if verifyReq.twitterId > 0:
            # find the twitter user with the specified twitter id
            user = User.findOrCreate('twitter', verifyReq.twitterId)
            
            # TODO: update the user details
            user.screenName = verifyReq.screenName
            user.profileImageUrl = verifyReq.profileImageUrl
            user.location = verifyReq.location
            user.utcOffset = verifyReq.utcOffset
            user.accessToken = verifyReq.accessToken
            user.put()
    
            # push the current user to the request so we can retrieve it in the middleware 
            # TODO: check if this is the best way to do this... kinda doesn't feel right...
            social_auth.persistUserSession(request, user)
            
        # return to the home page
        return render_to_response(request, 'social_auth/login_success.html')   
    except (twitter.TwitterAuthRequiredException), authError:
        return HttpResponseRedirect(authError.authorizationUrl)
        
def logout(request, next_page):
    """
    The logout handler for twitter authentication
    """
    
    logging.debug("Social methods supported are: %s", social_auth.getSupportedSites())
    
    return django_views.logout(request, next_page, 'social_auth/logout.html')
    
def fb_login(request):
    """
    This function will render the view for the successful Facebook login page.
    """

    try:    
        import facebook
        from django.conf import settings
        
        # if the request contains valid facebook cookies, then process
        fb = facebook.Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
        fb_data = fb.validate_cookie_signature(request.COOKIES)
        
        if not fb_data:
            raise Exception("Facebook support enabled, but no facebook user logged in")
        
        # add some extra data to the facebook object
        fb.session_key = fb_data['session_key']
        fb.uid = fb_data['user']
    
        logging.debug("Request contains Facebook cookie signature (from FBConnect) = %s", fb_data)
        
        fb_userdata = fb.users.getInfo(fb.uid, ['first_name', 'last_name', 'profile_url', 'pic_square'])
        logging.debug("User Data for logged in user = %s", fb_userdata)
        
        user = User.findOrCreate('facebook', fb.uid)

        # TODO: update the user details
        user.screenName = "%s %s" % (fb_userdata[0]['first_name'], fb_userdata[0]['last_name'])
        user.profileImageUrl = fb_userdata[0]['pic_square']
        user.accessToken = fb.session_key
        user.put()
        
        social_auth.persistUserSession(request, user)
                    
        return render_to_response(request, 'social_auth/facebook_login_ok.html')    
    except (Exception), inst:
        logging.error("Error validating facebook user: %s", inst)
        return render_to_response(request, 'social_auth/facebook_login_fail.html')
        
def fb_check_session(request):
    """
    This method is used to check that the facebook session is still valid for the currently logged in user
    """
    
    import facebook
    from django.conf import settings
    
    # if the request contains valid facebook cookies, then process
    fb = facebook.Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
    fb_data = fb.validate_cookie_signature(request.COOKIES)
    
    if not fb_data:
        raise Exception("Facebook support enabled, but no facebook user logged in")
        
    return render_to_response(request, 'social_auth/facebook_login_ok.html')
