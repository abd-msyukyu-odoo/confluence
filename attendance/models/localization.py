from django.db import models
from django.db.models import F

from .base import Model

class Localization(Model):
    """slot through contact (ManyToMany relation model)"""

    # Fields
    contact = models.ForeignKey(to='Contact', on_delete=models.CASCADE, help_text='Contact')
    slot = models.ForeignKey(to='Slot', on_delete=models.CASCADE, help_text='Slot')

    # Metadata
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot', 'contact'], name='unique_slot_contact')
        ]
        ordering = ['sequence']

    # Methods
    def __str__(self):
        return self.contact.name

    def sequence_filter():
        return {
            'contact': F('contact'),
            'slot': F('slot'),
        }
