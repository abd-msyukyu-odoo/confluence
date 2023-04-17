from django.db import models

from .presence import Presence

class TutorPresence(Presence):
    """presence for tutors"""

    # Fields
    slot = models.ForeignKey(to='Slot', on_delete=models.CASCADE, help_text='Slot')
    status = models.CharField(choices=Presence.STATUS_CHOICES, default=Presence.PRESENT, help_text='Status',
                              max_length=15)
    tutor = models.ForeignKey(to='Person', on_delete=models.CASCADE, help_text='Tutor')

    # Metadata
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot', 'tutor'], name='unique_slot_tutor')
        ]

    # Methods
    def __str__(self):
        return ' '.join([str(self.slot), str(self.tutor)])
