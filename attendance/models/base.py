from attendance.middleware.environment_middleware import Environment
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models import Max
import threading

def env_permission_required(perm):
    def permission_required(func):
        def wrapper(self, *args, **kwargs):
            if not self.id and not self.env.has_perm(self._meta.app_label + ('.%s_' % perm) + self._meta.model_name):
                raise PermissionDenied('You do not have the permission to %s a "%s", please ask an Administrator to help you with your request' % (perm, self._meta.model_name))
            return func(self, *args, **kwargs)
        return wrapper
    if perm in ['add', 'delete', 'change']:
        return permission_required
    else:
        raise Exception("Invalid decorator argument")

class Model(models.Model):
    """base model for default fields"""

    # Fields
    created_on = models.DateTimeField(auto_now_add=True, help_text='Creation Date')
    is_active = models.BooleanField(default=True, help_text='Active')
    sequence = models.PositiveBigIntegerField(blank=True, default=0, help_text='Sequence')
    updated_on = models.DateTimeField(auto_now=True, help_text='Last Update Date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        local = threading.local()
        self.env = local.env if hasattr(local, 'env') else Environment(None)

    # Metadata
    class Meta:
        """can be inherited by a child Meta class"""
        abstract = True

    # Methods
    @env_permission_required('delete')
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    @env_permission_required('add')
    @env_permission_required('change')
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
