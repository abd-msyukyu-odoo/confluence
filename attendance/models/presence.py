from django.db import models

from .base import Model

class Presence(Model):
    """
    base model for presences, may be useful with django-polymorphic:
    https://django-polymorphic.readthedocs.io/en/stable/
    -> with polymorphic, define a getter for "person" overridable by
    subclasses
    """
    PRESENT = 'P'
    ABSENT = 'A'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    # Fields
    # TODO think of a way to put slot here (constraint error)
