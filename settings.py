# Module:   social_auth.settings
# This module is used to initialise the settings for the social_auth app
# 
# Section:  Version History
# 08/09/2009 (DJO) - Created File

from ragendja.settings_post import settings

# add some additional css files to the combined files
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'social_auth/style.css',
)

# initialise the settings to include the social auth jquery library
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'social_auth/jquery.socialauth.js',
)

