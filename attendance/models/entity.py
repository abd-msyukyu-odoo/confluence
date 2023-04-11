from django.db import models

from .base import Model

class Entity(Model):
    """base model for entity relations (i.e. addresses)"""

    # Fields
    """contact_set""" # ManyToOne relation with contact (don't forget to use `prefetch_related` if necessary)
