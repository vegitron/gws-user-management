from django.core.management.base import BaseCommand, CommandError
from restclients.gws import GWS
from django.conf import settings
import pwd
import re
import os
from django.utils.log import getLogger

log = getLogger(__name__)


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
                        log.info("Adding user: %s" % username)
                        os.system("/usr/sbin/useradd -m %s" % username)
