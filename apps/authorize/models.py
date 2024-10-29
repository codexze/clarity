from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from apps.core.models import *

class FrontendPermission(models.Model):
    view_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    add_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    change_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    delete_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)

class User(AbstractUser):
    HELP_PW    = "Force this user to change their password on the next login"

    date_of_birth = models.DateField(blank=True, null=True)
    force_password_change = models.BooleanField(default=True, help_text=HELP_PW)
   
    class Meta:
        ordering = ('last_name', )
    
    @property
    def name(self):
        return self.get_full_name()

    def has_role(self, group):
        return self.groups.filter(name=group).exists()

    def eligible_for_reset(self):
        if not self.is_active:
            # if the user is active we dont bother checking
            return False

        return self.has_usable_password()

