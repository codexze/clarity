from django.db import models

from apps.authorize.models import User
from apps.authorize.manager import RoleManager

from apps.core.models import *

class Staff(User):
    objects = RoleManager()
    class Meta:
        proxy = True
        
class Service(Subrecord):
    name = models.CharField(max_length=255)
    duration = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    @property
    def display(self):
        time = ""
        if self.duration.hour > 0:
            time += f"{self.duration.hour} hour"

        if self.duration.minute > 0:
            time += f"{self.duration.minute} minutes"

        return f"{self.name} ({time})"

    def __str__(self):
        return self.display

class StaffServices(models.Model):
    employee = models.ForeignKey(Staff, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('employee', 'service')  
        
    def __str__(self):
        return f"{self.employee.name} ({self.service.name})"
