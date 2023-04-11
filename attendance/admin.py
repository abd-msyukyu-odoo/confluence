from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SlotTemplate)
admin.site.register(Institution)
admin.site.register(Attendee)
admin.site.register(Tutor)
admin.site.register(Contact)
admin.site.register(SlotTemplateOrganization)
admin.site.register(SlotTemplateSubscription)
admin.site.register(Slot)
admin.site.register(Localization)
admin.site.register(AttendeePresence)
admin.site.register(TutorPresence)
