import csv
import random

from contextlib import contextmanager

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models.fields import NOT_PROVIDED
from django.db import models, utils
from rest_framework.authtoken.models import Token

from attendance.models import *
from ._utils import *

class Command(BaseCommand):
    MODELS = {
        'slot_template': SlotTemplate,
        'institution': Institution,
        'person': Person,
        'contact': Contact,
        'slot_template_organization': SlotTemplateOrganization,
        'slot_template_subscription': SlotTemplateSubscription,
        'slot': Slot,
        'localization': Localization,
        'attendee_presence': AttendeePresence,
        'tutor_presence': TutorPresence,
        'user': User,
    }
    GROUPS = [{
            'name': 'row_attendant',
            'permissions': [],
        }, {
            'name': 'row_manager',
            'permissions': [],
        },
    ]

    @contextmanager
    def populate_context_manager(self, model):
        output = {
            'link': '',
            'source': [],
        }
        self.stdout.write(
            self.style.SUCCESS('Populate model %s ... ' % model._meta.model_name),
            ending=''
        )
        try:
            yield output
        finally:
            self.stdout.write(
                self.style.SUCCESS(output['link'].join(output['source']))
            )

    def add_arguments(self, parser):
        parser.add_argument("models", nargs="+", type=str)
        parser.add_argument(
            "--population",
            help="Base population per dependency (integer)",
        )
        parser.add_argument(
            "--noflush",
            action='store_true',
            help="Keep existing data",
        )

    def handle(self, *args, **kwargs):
        if not kwargs['noflush']:
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
            population = int(kwargs['population'])
        models = []
        for model in kwargs["models"]:
            if model == 'config':
                models = []
                break
            elif model == 'all':
                models = list(self.MODELS.keys())
                break
            try:
                models.append(self.MODELS[model])
            except KeyError:
                self.stderr.write(
                    self.style.ERROR('Model %s does not exist' % model)
                )

        # create system user
        with self.populate_context_manager(User) as output:
            system = User.objects.filter(username=settings.SYSTEM_USERNAME).first() or None
            if not system:
                system = User.objects.create_superuser(username=settings.SYSTEM_USERNAME)
                token = Token.objects.create(user=system)
                with open('.env', 'r+') as f:
                    content = f.readlines()
                    f.seek(0)
                    for line in content:
                        if line.startswith('SYSTEM_USER_TOKEN='):
                            f.write('SYSTEM_USER_TOKEN=%s\n' % token.key)
                        else:
                            f.write(line)
                    f.truncate()
                output['source'].append('created')
            else:
                output['source'].append('used')
            output['source'].append(' %s user' % settings.SYSTEM_USERNAME)

        # read permissions
        with open('attendance/models/_security.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            property_names = next(csv_reader)
            group_index = property_names.index('group_name')
            model_index = property_names.index('model_name')
            permission_indexes = [property_names.index(perm) for perm in ['add', 'delete', 'change', 'view']]
            for row in csv_reader:
                for group in self.GROUPS:
                    if group['name'] == row[group_index]:
                        Model = self.MODELS[row[model_index]]
                        for perm_index in permission_indexes:
                            if not int(row[perm_index]):
                                continue
                            permission = Permission.objects.get_by_natural_key(
                                '%s_' % property_names[perm_index] + Model._meta.model_name,
                                Model._meta.app_label,
                                Model._meta.model_name
                            )
                            group['permissions'].append(permission)

        # create group instances
        with self.populate_context_manager(Group) as output:
            output['link'] = ', '
            for group_data in self.GROUPS:
                group, create = Group.objects.get_or_create(name=group_data['name'])
                group.permissions.add(*group_data['permissions'])
                operation = 'created' if create else 'used'
                output['source'].append('%s %s' % (operation, group.name))

        # create model instances
        for key, model in list(self.MODELS.items()):
            if key in models and key != 'user':
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

        with self.populate_context_manager(model) as output:
            for record_fields in records_fields:
                try:
                    # TODO NVI find a way to bulk_create
                    model.objects.create(**record_fields)
                except utils.IntegrityError:
                    # TODO NVI proper way of avoiding integrity constraints error
                    continue
            output['source'].append('done')
