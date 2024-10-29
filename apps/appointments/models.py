from django.db import models

from apps.clients.models import Client
from apps.services.models import Staff, Service

from apps.core.models import *

DATE_FORMAT_REVERSED = "%Y-%m-%d"
WEEKDAY_FORMAT = "%A"

class Slot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
      ordering = ['start']

    # @property
    # def weekday(self):
    #     return self.start.strftime(WEEKDAY_FORMAT)

    # @property
    # def allday(self):
    #     return self.start.strftime(DATE_FORMAT_REVERSED)

    class Meta:
        abstract = True

class Appointment(Slot, Subrecord):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2) # this save the price in time, useful for reporting
    employee = models.ForeignKey(Staff, on_delete=models.PROTECT)
    
    is_walkin = models.BooleanField(default=False) # tells us if it was a last minute booking, useful for reporting

    arrived = models.BooleanField(default=False)
    arrived_time = models.TimeField(null=True, blank=True) # helpfull to know

    cancelation = models.BooleanField(default=False) # helpfull to know
    cancelation_reason = models.CharField(max_length=255) # helpfull to know
