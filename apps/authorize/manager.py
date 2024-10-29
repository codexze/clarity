from django.db import models
from django.db.models import Q

class RoleManager(models.Manager):
    def base(self):
        return super().get_queryset().filter(is_active=True)
    
    def role(self, role):
        return self.base().filter(groups__name=role)
    
    def app_admin(self):
        return self.role('app_admin')
    
    def adminitration(self):
        return self.role('administration')

    def employee(self):
        return self.role('employee')