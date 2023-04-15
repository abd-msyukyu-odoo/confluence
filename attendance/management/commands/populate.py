import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models.fields import NOT_PROVIDED
from django.db import models, transaction, utils

from attendance.models import *
from ._utils import *

class Command(BaseCommand):
    MODELS = {
        'slot_template': SlotTemplate,
        'institution': Institution,
        'attendee': Attendee,
        'tutor': Tutor,
        'contact': Contact,
        'slot_template_organization': SlotTemplateOrganization,
        'slot_template_subscription': SlotTemplateSubscription,
        'slot': Slot,
        'localization': Localization,
        'attendee_presence': AttendeePresence,
        'tutor_presence': TutorPresence,
    }

    def add_arguments(self, parser):
        parser.add_argument("models", nargs="+", type=str)
        parser.add_argument(
            "--population",
            help="Base population per dependency (integer)",
        )

    def handle(self, *args, **kwargs):
        # empty the database
        self.stdout.write(
            self.style.NOTICE('Database flush ... '),
            ending=''
        )
        call_command('flush', '--noinput')
        self.stdout.write(
            self.style.NOTICE('done'),
        )

        population = None
        if kwargs['population']:
            population = kwargs['population']
        models = []
        for model in kwargs["models"]:
            if model == 'all':
                models = list(self.MODELS.keys())
                break
            try:
                models.append(self.MODELS[model])
            except KeyError:
                self.stderr.write(
                    self.style.ERROR('Model %s does not exist' % model)
                )

        for key, model in list(self.MODELS.items()):
            if key in models:
                self.populate(model, population)

    def populate(self, model, population=5):
        if not population:
            population = 5
        base_population = population

        dependencies = {field.name: {
            'count': 0,
            'instance': field,
        } for field in model._meta.get_fields() if isinstance(field, models.ForeignKey) and not issubclass(model, field.related_model)}
        for field in dependencies.values():
            field['count'] = field['instance'].related_model.objects.count()
            population = max(population, base_population * field['count'])

        records_fields = []
        for _ in range(population):
            fields = {}
            for field in model._meta.get_fields():
                if (hasattr(field, 'default') and field.default != NOT_PROVIDED) or (
                    hasattr(field, 'auto_now') and field.auto_now) or (
                    hasattr(field, 'auto_now_add') and field.auto_now_add):
                    continue
                value = NOT_PROVIDED
                if type(field) is models.ForeignKey and not issubclass(model, field.related_model):
                    entry_index = random.randint(0, dependencies[field.name]['count'] - 1)
                    value = field.related_model.objects.all()[entry_index]
                elif type(field) is models.CharField:
                    if Contact.phone_regex in field.validators:
                        value = generate_random_phone()
                    else:
                        value = generate_random_word()
                elif type(field) is models.EmailField:
                    value = generate_random_email()
                elif type(field) is models.DateField:
                    value = generate_random_date()
                elif type(field) is models.DateTimeField:
                    if field.name.startswith('start_'):
                        opposite = 'end_' + field.name.split('start_')[1]
                        if opposite in fields:
                            value = generate_random_datetime(after=fields[opposite])
                    elif field.name.startswith('end_'):
                        opposite = 'start_' + field.name.split('end_')[1]
                        if opposite in fields:
                            value = generate_random_datetime(before=fields[opposite])
                    value = generate_random_datetime() if value == NOT_PROVIDED else value
                elif type(field) is models.PositiveIntegerField:
                    value = generate_random_positive_integer()
                elif type(field) is models.BooleanField:
                    value = generate_random_boolean()
                if value != NOT_PROVIDED:
                    fields[field.name] = value
            records_fields.append(fields)

        self.stdout.write(
            self.style.SUCCESS('Populate model %s ... ' % model._meta.model_name),
            ending=''
        )
        for record_fields in records_fields:
            try:
                model.objects.create(**record_fields)
            except utils.IntegrityError:
                # TODO proper way of avoiding integrity constraints error
                continue
        self.stdout.write(
            self.style.SUCCESS('done')
        )
