from django.db import models

from .base import Model

class SlotTemplateSubscription(Model):
    """attendee subscription to a slot template"""

    # Fields
    attendee = models.ForeignKey(to='Person', on_delete=models.CASCADE, help_text='Attendee')
    slot_template = models.ForeignKey(to='SlotTemplate', on_delete=models.CASCADE, help_text='Slot Template')
    subscribed = models.BooleanField(default=True, help_text='subscribed')

    # Metadata
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot_template', 'attendee'], name='unique_slot_template_attendee')
        ]

    # Methods
    def __str__(self):
        return ' '.join([str(self.slot_template), str(self.attendee)])
