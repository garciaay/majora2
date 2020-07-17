from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from majora2 import models
from django.contrib.auth.models import User, Permission

from tatl import models as tmodels
from majora2 import models as models

import sys
import json

class Command(BaseCommand):
    help = "Grant dataview access to a user"
    def add_arguments(self, parser):
        parser.add_argument('dataview')
        parser.add_argument('user')

    def handle(self, *args, **options):
        su = User.objects.get(is_superuser=True)
        try:
            mdv = models.MajoraDataview.objects.get(code_name=options["dataview"])
        except:
            print("No dataview with that name.")
            sys.exit(1)

        try:
            user = User.objects.get(username=options["user"])
        except:
            print("No user with that username.")
            sys.exit(1)

        p = models.MajoraDataviewUserPermission(
                profile = user.profile,
                dataview = mdv,
                validity_start = timezone.now(),
                #validity_end = 
        )
        treq = tmodels.TatlPermFlex(
            user = su,
            substitute_user = None,
            used_permission = "tatl.management.commands.grant_dataview",
            timestamp = timezone.now(),
            content_object = user.profile,
            extra_context = json.dumps({
                "dataview": mdv.code_name
            }),
        )
        treq.save()
