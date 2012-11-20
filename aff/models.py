from django.db import models

class ActiveRegion(models.Model):
    country = models.CharField(max_length=40, verbose_name="Country", blank=True, null=True)
    region = models.CharField(max_length=40, verbose_name="Region", blank=True, null=True)
    def __unicode__(self):
        return self.region



