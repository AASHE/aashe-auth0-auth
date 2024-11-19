from django.db import models
from django.utils.translation import gettext_lazy as _

class Organization(models.Model):
    id = models.CharField(_("Auth0 Organization ID"), max_length=255, primary_key=True)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
    
    def __str__(self):
        return self.name
