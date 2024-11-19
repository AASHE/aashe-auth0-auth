from django.db import models

class Organization(models.Model):
    id = models.models.CharField(_("Auth0 Organization ID"), max_length=255, primary_key=True)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=255)
    metadata = models.JSONField(default={})

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
    
    def __str__(self):
        return self.name
