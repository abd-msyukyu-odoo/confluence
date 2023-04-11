from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # this auto creates the id field for each model (primary_key)
    name = 'attendance'
