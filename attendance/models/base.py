from django.db import models, transaction
from django.db.models import Max

class Model(models.Model):
    """base model for default fields"""

    # Fields
    archived = models.BooleanField(default=False, help_text='Archived')
    created_on = models.DateTimeField(auto_now_add=True, help_text='Creation Date')
    sequence = models.PositiveBigIntegerField(blank=True, default=0, help_text='Sequence')
    updated_on = models.DateTimeField(auto_now=True, help_text='Last Update Date')

    # Metadata
    class Meta:
        """can be inherited by a child Meta class"""
        abstract = True

    # Methods
    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)
        if not self.sequence:
            self.sequence = (self.__class__.objects.aggregate(Max('sequence'))['sequence__max'] or 0) + 1
            if update_fields and not 'sequence' in update_fields:
                update_fields.append('sequence')
        else:
            sequence = self.sequence
            filters = self.sequence_filter()
            filters['sequence__gte'] = sequence
            records = self.__class__.objects.exclude(id=self.id).filter(**filters).order_by('sequence')
            with transaction.atomic():
                for record in records:
                    if sequence == record.sequence:
                        sequence += 1
                        self.__class__.objects.filter(id=record.id).update(sequence=sequence)
                    else:
                        break
        super().save(*args, **kwargs)

    def sequence_filter():
        """
        The sequence applies on every record of a Model by default.
        This filter allows to specify a granularity so that the sequence applies
        on a subset of records.
        """
        return {}
