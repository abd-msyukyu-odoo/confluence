from django.db import models

from .entity import Entity

class Institution(Entity):
    """entity (i.e. school, cultural center)"""

    # Fields
    name = models.CharField(help_text='Name', max_length=255)

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name
