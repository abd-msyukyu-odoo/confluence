from django.db import models

from .presence import Presence

class AttendeePresence(Presence):
    """presence for attendees"""
    UNKNOWN = 'U'
    STATUS_CHOICES = Presence.STATUS_CHOICES + [
        (UNKNOWN, 'Unknown'),
    ]

    # Fields
    attendee = models.ForeignKey(to='Attendee', on_delete=models.CASCADE, help_text='Attendee')
    slot = models.ForeignKey(to='Slot', on_delete=models.CASCADE, help_text='Slot')
    status = models.CharField(choices=STATUS_CHOICES, default=Presence.PRESENT, help_text='Status', max_length=15)

    # Metadata
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot', 'attendee'], name='unique_slot_attendee')
        ]

    # Methods
    def __str__(self):
        return ' '.join([str(self.slot), str(self.attendee)])
