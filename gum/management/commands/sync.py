from django.core.management.base import BaseCommand, CommandError
from restclients.gws import GWS
from django.conf import settings
import pwd
import re
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        group_id = settings.GUM_GWS_GROUP

        members = GWS().get_effective_members(group_id)

        for member in members:
            if member.is_uwnetid():
                try:
                    values = pwd.getpwnam(member.name)
                except KeyError as ex:
                    username = member.name
                    if re.match(r'^[0-9a-z]+$', username):
                        os.system("/usr/sbin/useradd -m %s" % username)
