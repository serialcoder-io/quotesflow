# managers.py
from django.db import models

class OrganizationManager(models.Manager):
    def for_org(self, org):
        return self.get_queryset().filter(organization=org)
