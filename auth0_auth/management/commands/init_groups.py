#!/usr/bin/env python
"""
Syncs orgs from Auth0.
"""
import logging, os, json, requests, time
from django.conf import settings

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from auth0_auth.backends import OIDCToDjangoGroupsMapping

logger = logging.getLogger(os.path.basename(__file__))


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_groups()
    

def init_groups():
    """
        Creates all configured django groups and gives all perms to staff group
    """
    django_groups = OIDCToDjangoGroupsMapping.get_all_django_groups()

    for group_name in django_groups:
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            print(f"Created group {group_name}")

        if group_name == "staff":
            print(f"Adding all permissions to group {group_name}")
            for perm in Permission.objects.all():
                group.permissions.add(perm)

            group.save()

    print("Done.")
