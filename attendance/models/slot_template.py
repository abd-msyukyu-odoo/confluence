from django.db import models

from .base import Model

class SlotTemplate(Model):
    """configuration for slots (registrations, occurrences, ...)"""

    # Fields
    attendees = models.ManyToManyField(to='Attendee', blank=True, help_text='Attendees', related_name='+',
                                       through='SlotTemplateSubscription', through_fields=('slot_template', 'attendee'))
    name = models.CharField(help_text='Name', max_length=255)
    """slot_set""" # ManyToOne relation with slot
    tutors = models.ManyToManyField(to='Tutor', blank=True, help_text='Tutors', related_name='+',
                                    through='SlotTemplateOrganization', through_fields=('slot_template', 'tutor'))

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name
