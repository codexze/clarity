import random
from django.utils import timezone

from django.db import models
from django.conf import settings

from . import exceptions


class Singleton(models.Model):
    """A base class for Singleton models."""

    class Meta:
        abstract = True  # This ensures it won't create a separate database table.

    def save(self, *args, **kwargs):
        """Override the save method to ensure only one instance exists."""
        self.pk = 1  # Enforce the primary key as 1 for uniqueness.
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the single instance of the model or create it if none exists."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    

class Subrecord(models.Model):
    """
    Abstract base model for records that require tracking of consistency, 
    creation, and updates along with the user responsible for those actions.
    """

    # A token to ensure data integrity, generated randomly as an 8-character hex string
    consistency_token = models.CharField(max_length=8)

    def set_consistency_token(self):
        """Generate and assign a random 8-character hex string to the consistency_token."""
        self.consistency_token = '%08x' % random.randrange(16**8)

    # Timestamps for tracking when the record was created and last updated
    created = models.DateTimeField(blank=True, null=True)  # Creation timestamp
    updated = models.DateTimeField(blank=True, null=True)  # Update timestamp

    # Foreign keys to reference the user who created and last updated the record
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Links to Django's user model
        blank=True, null=True,  # Allows the field to be empty
        related_name="created_%(app_label)s_%(class)s_subrecords",  # Dynamic related name
        on_delete=models.SET_NULL  # Keeps the record even if the user is deleted
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Links to the user who last updated the record
        blank=True, null=True,
        related_name="updated_%(app_label)s_%(class)s_subrecords",  # Dynamic related name
        on_delete=models.SET_NULL  # Prevent deletion of the subrecord if user is removed
    )

    def set_created_by_id(self, incoming_value, user, *args, **kwargs):
        """
        Set the 'created_by' field to the given user only if the record is new.
        """
        if not self.id:  # Only assign on first save
            self.created_by = user

    def set_updated_by_id(self, incoming_value, user, *args, **kwargs):
        """
        Update the 'updated_by' field to the given user if the record already exists.
        """
        if self.id:  # Only assign if the record exists
            self.updated_by = user

    def set_updated(self, incoming_value, user, *args, **kwargs):
        """
        Set the 'updated' timestamp to the current time if the record exists.
        """
        if self.id:  # Only set if the record exists
            self.updated = timezone.now()

    def set_created(self, incoming_value, user, *args, **kwargs):
        """
        Set the 'created' timestamp to the current time if the record is new.
        """
        if not self.id:  # Only set on the first save
            self.created = timezone.now()

    def update_from_kwargs(self, **kwargs):
        """
        Update the fields of the record based on keyword arguments.
        Ensure the provided consistency token matches the current one.
        """
        if self.consistency_token:  # Check if token is set
            try:
                consistency_token = kwargs.pop('consistency_token')  # Extract the token
            except KeyError:
                # Raise an exception if the token is missing
                msg = 'Missing field (consistency_token) for {}'
                raise exceptions.MissingConsistencyTokenError(
                    msg.format(self.__class__.__name__)
                )

            # Raise an error if the token does not match
            if consistency_token != self.consistency_token:
                raise exceptions.ConsistencyError

        # Update model fields with the remaining kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)  # Dynamically set attributes

        self.save()  # Save the updated record

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure a new consistency token is generated
        each time the record is saved.
        """
        self.set_consistency_token()  # Refresh token on every save
        super(Subrecord, self).save(*args, **kwargs)  # Call the parent save method

    class Meta:
        abstract = True  # This model will not create a table on its own.

class LookupList(models.Model):
    """A base class for Lookup list."""

    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('key', 'value')  # Prevent duplicate entries
        ordering = ['value']
        abstract = True

    def __str__(self):
        return f"{self.key}: {self.value}"
