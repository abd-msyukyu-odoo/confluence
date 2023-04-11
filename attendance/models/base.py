from django.db import models

class Model(models.Model):
    """base model for default fields"""

    # Fields
    archived = models.BooleanField(default=False, help_text='Archived')
    created_on = models.DateTimeField(auto_now_add=True, help_text='Creation Date')
    updated_on = models.DateTimeField(auto_now=True, help_text='Last Update Date')

    # Metadata
    class Meta:
        """can be inherited by a child Meta class"""
        abstract = True
