from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Authentication models.
admin.site.register(User, UserAdmin)
# Custom models.
admin.site.register(SlotTemplate)
admin.site.register(Institution)
admin.site.register(Person)
admin.site.register(Contact)
admin.site.register(SlotTemplateOrganization)
admin.site.register(SlotTemplateSubscription)
admin.site.register(Slot)
admin.site.register(Localization)
admin.site.register(AttendeePresence)
admin.site.register(TutorPresence)
