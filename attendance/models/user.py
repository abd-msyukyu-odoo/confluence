from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """(attendance) user"""

    #Fields
    person = models.ForeignKey(to='Person', on_delete=models.SET_NULL, blank=True,
                               help_text='Person', null=True, related_name='user_set')

    # Metadata
    class Meta:
        constraints = [
            models.CheckConstraint(check=~Q(username=settings.SYSTEM_USERNAME) | Q(person=None),
                                   name='%s_person_is_none' % settings.SYSTEM_USERNAME.lower())
        ]
