from django.db import models
from mezzanine.core.models import Displayable, RichTextField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User



class ActiveRegion(models.Model):
    country = models.CharField(max_length=40, verbose_name="Country", blank=True, null=True)
    region = models.CharField(max_length=40, verbose_name="Region", blank=True, null=True)
    def __unicode__(self):
        return self.region


class PropertyDescription(Displayable):
    address1 = models.CharField(max_length=400, verbose_name="Address", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="City", blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name="State", blank=True, null=True)
    square_feet = models.CharField(max_length=10, verbose_name="Square footage", blank=True, null=True)
    number_of_bedrooms = models.CharField(max_length=10, verbose_name="Number of bedrooms", blank=True, null=True)
    number_of_bathrooms = models.CharField(max_length=10, verbose_name="Number of bathrooms", blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

#    @models.permalink
#    def get_absolute_url(self):
#       return ('gohotels.views.detail', [self.slug, self.hotelid])

#    def save(self, *args, **kwargs):
#       self.point = Point(float(self.longitude), float(self.latitude))
#       super(HotelPage, self).save(*args, **kwargs)

    def __unicode__(self):
       return self.title


class PropertyImage(models.Model):
    img = models.ImageField(upload_to="uploads", blank=True, null=True, default='uploads/default.png')
    property = models.ForeignKey(PropertyDescription, blank=True, null=True)

    def __unicode__(self):
        return self.img





