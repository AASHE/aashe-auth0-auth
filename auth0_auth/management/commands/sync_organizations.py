#!/usr/bin/env python
"""
Syncs orgs from Auth0.
"""
import logging, os, json, requests, time
from django.conf import settings

from django.core.management.base import BaseCommand

from auth0_auth.api_client import Auth0APIClient
from auth0_auth.models import Organization

logger = logging.getLogger(os.path.basename(__file__))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--sync-all',
            action='store_true',
            dest='sync-all',
            default=False,
            help='Sync all organizations',
        )

    def handle(self, *args, **options):
        sync_auth0_organizations(sync_all=options['sync-all'])
    

def sync_auth0_organizations(sync_all=False):
    """
        Syncs 100 last created orgs from Auth0
        Use --sync-all for everything
    """

    client = Auth0APIClient(settings.AUTH0_DOMAIN, settings.OIDC_RP_CLIENT_ID, settings.OIDC_RP_CLIENT_SECRET)

    orgs = client.list_organizations(fetch_all=sync_all)

    created = 0
    for org in orgs:
        instance, _ = Organization.objects.get_or_create(
            id=org["id"], 
            defaults={
                "name": org["name"], 
                "display_name": org["display_name"], 
                "metadata": org["metadata"] if "metadata" in org else {}
            }
        )
        if _: 
            created += 1

    print(f"Created {created} new organizations.")
    print("Done.")
