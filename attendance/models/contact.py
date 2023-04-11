from django.core.validators import RegexValidator
from django.db import models

from .base import Model

class Contact(Model):
    """contact infos for an entity"""

    # Validators
    # https://en.wikipedia.org/wiki/E.164
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message='Phone number format should be: "+32123456789". Up to 15 digits allowed.')

    # Fields
    city = models.CharField(blank=True, help_text='City', max_length=255)
    country = models.CharField(blank=True, help_text='Country', max_length=255)
    entity = models.ForeignKey(to='Entity', on_delete=models.CASCADE, help_text='Contact Holder', related_name='contact_set')
    name = models.CharField(help_text='Name', max_length=255)
    phone = models.CharField(blank=True, help_text='Phone Number', max_length=16, validators=[phone_regex])
    email = models.EmailField(blank=True, help_text='Email')
    state = models.CharField(blank=True, help_text='State', max_length=255)
    street = models.CharField(blank=True, help_text='Street', max_length=255)
    zip_code = models.CharField(blank=True, help_text='Zip', max_length=255)

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name
