from django.db import models

from .person import Person

class Tutor(Person):
    """person (holding slots)"""

    # Fields

    # Metadata
    class Meta:
        ordering = ['last_name', 'first_name']

    # Methods
    def __str__(self):
        return ' '.join([self.last_name, self.first_name])
