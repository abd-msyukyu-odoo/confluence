from django.db import models

from .entity import Entity

class Person(Entity):
    """entity (human)"""

    # Fields
    birthdate = models.DateField(blank=True, help_text='Birthdate', null=True)
    first_name = models.CharField(help_text='First Name', max_length=255)
    last_name = models.CharField(help_text='Last Name', max_length=255)
    """user_set""" # ManyToOne relation with user

    # Metadata
    class Meta:
        ordering = ['last_name', 'first_name']

    # Methods
    def __str__(self):
        return ' '.join([self.last_name, self.first_name])
