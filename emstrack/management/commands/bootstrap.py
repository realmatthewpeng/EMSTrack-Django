from django.contrib.auth import get_user_model

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.db import DEFAULT_DB_ALIAS
from django.db import IntegrityError

from django.db.models import F, Value
from django.db.models.functions import Coalesce

from ambulance.models import Ambulance
from login.models import Organization

class Command(BaseCommand):

    help = 'Create admin user'

    def create_user(self, user, type_of_user, **options):

        # Retrieve current user model
        model = get_user_model()
        username_field = model._meta.get_field(model.USERNAME_FIELD)

        user_data = {}
        username = username_field.clean(user['USERNAME'], None)
        database = DEFAULT_DB_ALIAS

        if not username:
            raise CommandError("Could not retrieve '{}' from settings.".format(model.USERNAME_FIELD))

        # Make sure mandatory fields are present
        for field_name in model.REQUIRED_FIELDS:
            if user[field_name.upper()]:
                field = model._meta.get_field(field_name)
                user_data[field_name] = field.clean(user[field_name.upper()], None)
            else:
                raise CommandError("Could not retrieve '{}' from settings.".format(field_name))

        if username:

            # create superuser
            user_data[model.USERNAME_FIELD] = username
            user_data['password'] = user['PASSWORD']
            if type_of_user == 'admin':
                u = model._default_manager.db_manager(database).create_superuser(**user_data)
            else:
                u = model._default_manager.db_manager(database).create_user(**user_data)

            if type_of_user == 'guest':
                u.userprofile.is_guest = True
                u.userprofile.save()

            if options['verbosity'] >= 1:
                self.stdout.write(
                    self.style.SUCCESS("{} created successfully.".format(type_of_user)))

    def handle(self, *args, **options):

        if options['verbosity'] >= 1:
            self.stdout.write('Bootstraping ambulance application')
        
        # Retrieve defaults from settings
        superuser = {
            'USERNAME': '',
            'PASSWORD': '',
        }
        superuser.update(settings.MQTT)

        guestuser = {
            'USERNAME': '',
            'PASSWORD': '',
        }
        guestuser.update(settings.GUEST)

        try:

            # create superuser
            self.create_user(superuser, 'admin', **options)

        except IntegrityError as e:
            self.stdout.write(self.style.WARNING("Superuser already exists."))

        try:

            # create guest user
            self.create_user(guestuser, 'guest', **options)

        except IntegrityError as e:
            self.stdout.write(self.style.WARNING("Guest user already exists."))

        # Create or get the general organization
        general_organization, _ = Organization.objects.get_or_create(name='Unassigned')

        # Update existing ambulances to point to the general organization
        Ambulance.objects.filter(organization__isnull=True).update(
            organization=Coalesce('organization_id', Value(general_organization.id))
        )

        if options['verbosity'] >= 1:
            self.stdout.write(
                self.style.SUCCESS("Done."))
