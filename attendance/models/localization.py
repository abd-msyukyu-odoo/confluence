from django.db import models, transaction

from .base import Model

class Localization(Model):
    """slot through contact (ManyToMany relation model)"""

    # Fields
    contact = models.ForeignKey(to='Contact', on_delete=models.CASCADE, help_text='Contact')
    sequence = models.PositiveBigIntegerField(blank=True, default=0, help_text='Sequence')
    slot = models.ForeignKey(to='Slot', on_delete=models.CASCADE, help_text='Slot')

    # Metadata
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot', 'contact'], name='unique_slot_contact')
        ]
        ordering = ['sequence']

    # Methods
    def __str__(self):
        return self.contact.name

    def save(self, *args, **kwargs):
        update_fields = kwargs.setdefault('update_fields', [])
        if not self.sequence:
            localizations = Localization.objects.filter(contact=self.contact, slot=self.slot)
            if self.id:
                localizations.exclude(id=self.id)
            self.sequence = localizations.order_by('-sequence').first() + 1 or 1
            if 'sequence' not in update_fields:
                update_fields.append('sequence')
        elif 'sequence' in update_fields:
            localizations = Localization.objects.filter(contact=self.contact, slot=self.slot, sequence__gte=self.sequence).order_by('sequence')
            if self.id:
                localizations.exclude(id=self.id)
            with transaction.atomic():
                sequence = self.sequence
                for localization in localizations:
                    if sequence == localization.sequence:
                        sequence += 1
                        Localization.objects.filter(id=localization.id).update(sequence=sequence)
                    else:
                        break
        super().save(*args, **kwargs)
