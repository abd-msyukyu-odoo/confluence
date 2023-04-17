from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """(attendance) user"""

    #Fields
    person = models.ForeignKey(to='Person', on_delete=models.SET_NULL, blank=True,
                               help_text='Person', null=True, related_name='user_set')
