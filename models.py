# Package:  social_auth.models
# This package is used to define models that support the twitter based authentication for the site.  This package
# uses the technique as explained @ http://code.google.com/p/app-engine-patch/wiki/CustomUserModel to create a
# custom user model that expresses the information that is associated with a twitter user.
# 
# Section:  Version History
# 09/06/2009 (DJO) - Created File
#
# Section: Credits
# Based on the implementation seen in ragenda.auth.google_models

# import standard libraries
import datetime
import logging

# import appengine libraries
from google.appengine.ext import db
from google.appengine.api import memcache
from ragendja.auth.models import UserTraits
from django.utils.translation import ugettext_lazy as _

class SocialUserTraits(UserTraits):
    """
    This class defines the methods and attributes for defining and authenticating a twitter user
    """
    
    # initialise properties
    screenName = db.StringProperty(required = False)
    email = db.StringProperty(required = False)
    profileImageUrl = db.StringProperty(required = False)
    location = db.StringProperty(required = False)
    utcOffset = db.IntegerProperty(required = False)
    
    def check_password(self, raw_password):
        """
        The check password method for the twitter user traits simply returns true as the password is not important.
        All that is important is that we trust the user is who they say they are.
        """
        
        # TODO: check if extra security is required here
        return True
    
    @classmethod
    def get_djangouser_for_user(cls, social_user):
        logging.debug("getting the django use for the specified social user: %s", social_user)
        
        if social_user and social_user.userId:
            # initialis the query to find the user
            django_user_query = cls.gql("WHERE userStore = :store AND userId = :id", store=social_user.userStore,id=social_user.userId)
        
            # locate the user
            django_user = django_user_query.get()
            if not django_user:
                django_user = cls.create_djangouser_for_user(twitter_user)
                django_user.is_active = True
                if getattr(settings, 'AUTH_ADMIN_USER_AS_SUPERUSER', True) and users.is_current_user_admin():
                    django_user.is_staff = True
                    django_user.is_superuser = True
                    
                django_user.put()
                
            logging.debug("django user = %s", django_user)
            return django_user
            
        # is this required, or is this the default for python
        return None
        
    class Meta:
        abstract = True    
    
class User(SocialUserTraits):
    """
    Extended user class that collects details for a twitter user in addition to standard user details
    """
    
    userStore = db.StringProperty(required = True)
    userId = db.StringProperty(required = True)       
   
    @staticmethod
    def findOrCreate(service_name, service_id):
        """
        This method is used to find the required twitter user specified by the twitter id
        """
        
        # initialise the query
        query = User.gql("WHERE userStore = :store AND userId = :id", store=service_name,id=service_id)

        # return the query result
        fnresult = query.get()
        
        # if the user is not found, then create the user
        if fnresult is None:
            fnresult = User(userStore = service_name, userId = str(service_id))
            fnresult.put()
            
        return fnresult

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def username(self):
        return "%s-%s" % (self.userStore, self.userId)
        
    @classmethod
    def create_djangouser_for_user(cls, user):
        return cls(userStore = cls.userStore, userId = user.userId)
        
class SocialProfile(db.Model):
    """
    This model encapsulates the details for a particular users social profile 
    details in the application.  A user can add social profiles and associate 
    them with a user on the system.
    """
    
    profileStore = db.StringProperty(required = True)
    profileId = db.StringProperty(required = True)
    profileUser = db.ReferenceProperty(User, required = True)
    
    # initialise the access token property
    # the type of access token will differ from platform to platform, but in 
    # general most distributed authentication systems use one to enable users
    # to persist sessions.
    accessToken = db.StringProperty(required = False)
