# Module:    twitter_auth.admin
# This module is used to define an administration module for the twitter user type

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class UserAdmin(admin.ModelAdmin):
    """
    The customized twitter user administration information
    """
    fieldsets = (
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    list_display = ('screenName', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('screenName',)
    filter_horizontal = ('user_permissions',)
