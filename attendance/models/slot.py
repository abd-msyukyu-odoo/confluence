from django.db import models
from django.db.models import F, Q

from .base import Model

class Slot(Model):
    """planned activity with a finite duration involving persons"""

    # Fields
    attendee_presences = models.ManyToManyField(to='Attendee', blank=True, help_text='Attendees presences',
                                                related_name='+', through='AttendeePresence',
                                                through_fields=('slot', 'attendee'))
    end_time = models.DateTimeField(blank=True, help_text='End Time', null=True)
    localizations = models.ManyToManyField(to='Contact', blank=True, help_text='Localizations', related_name='+',
                                           through='Localization', through_fields=('slot', 'contact'))
    name = models.CharField(help_text='Name', max_length=255)
    # eventually add sequence
    slot_template = models.ForeignKey(to='SlotTemplate', on_delete=models.SET_NULL, blank=True, help_text='Template',
                                      null=True, related_name='slot_set')
    start_time = models.DateTimeField(blank=True, help_text='Start Time', null=True)
    tutor_presences = models.ManyToManyField(to='Tutor', blank=True, help_text='Tutors presences', related_name='+',
                                             through='TutorPresence', through_fields=('slot', 'tutor'))

    # Metadata
    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(start_time__lte=F('end_time')), name='start_time_lte_end_time')
        ]
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name
