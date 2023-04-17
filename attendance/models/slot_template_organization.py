from django.db import models

from .base import Model

class SlotTemplateOrganization(Model):
    """tutor organization for a slot template"""

    # Fields
    slot_template = models.ForeignKey(to='SlotTemplate', on_delete=models.CASCADE, help_text='Slot Template')
    tutor = models.ForeignKey(to='Person', on_delete=models.CASCADE, help_text='Tutor')
    max_attendees = models.PositiveIntegerField(blank=True, help_text='Amount of attendees manageable by the Tutor', null=True)

    # Metadata
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot_template', 'tutor'], name='unique_slot_template_tutor')
        ]

    # Methods
    def __str__(self):
        return ' '.join([str(self.slot_template), str(self.tutor)])
