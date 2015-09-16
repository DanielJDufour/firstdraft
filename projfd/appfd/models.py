#-*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.gis.db.models import *

class Alert(Model):
    colors = (("danger", "danger"),("info", "info"),("success", "success"),("warning","warning"))
    color = CharField(choices=colors, max_length=200)
    permanent = BooleanField()
    text = CharField(max_length=200)
    user = OneToOneField(User, blank=True, null=True)
    def __str__(self):
        return self.text

class Calls(Model):
    date = DateField()
    total = IntegerField(default=0)
    CHOICES = [('gt', "Google Translate API")]
    service = CharField(max_length=200, choices=CHOICES)

class Activation(Model):
    created = DateTimeField(auto_now_add=True)
    expired = BooleanField(default=False)
    key = CharField(max_length=200)
    notified_success = BooleanField(default=False)
    used = BooleanField(default=False)
    user = OneToOneField(User)
    def __str__(self):
        return str(self.key[:10]) + "..."

class Alias(Model):
    alias = CharField(max_length=200, null=True, blank=True)
    entered = DateTimeField(auto_now_add=True)
    language = CharField(max_length=2)
    def __str__(self):
        return self.alias.encode("utf-8")
    class Meta:
        ordering = ['alias']

class AliasPlace(Model):
    alias = ForeignKey('Alias')
    place = ForeignKey('Place')

    class Meta:
        unique_together = (("alias","place"))


class Email(Model):
    address = EmailField(null=True, blank=True)
    entered = DateTimeField(auto_now_add=True)

class GeoName(Model):
    geonameid = IntegerField(primary_key=True)
    name = CharField(max_length=200, null=True, blank=True)
    asciiname = CharField(max_length=200, null=True, blank=True)
    alternatenames = CharField(max_length=10000, null=True, blank=True)
    latitude = DecimalField(decimal_places=10, max_digits=50)
    longitude = DecimalField(decimal_places=10, max_digits=50)
    feature_class = CharField(max_length=1)
    feature_code = CharField(max_length=10)
    country_code = CharField(max_length=2)
    cc2 = CharField(max_length=200)
    admin1_code = CharField(max_length=20)
    admin2_code = CharField(max_length=80)
    admin3_code = CharField(max_length=20)
    admin4_code = CharField(max_length=20)
    population = BigIntegerField()
    elevation = CharField(max_length=200)
    dem = BigIntegerField()
    timezone = CharField(max_length=40)
    modification_date = DateField()

class Order(Model):
    token = CharField(max_length=200, null=True, blank=True)

# should add in org and person model at some point, so can cross locate story based on people or orgs if no location names given

class Place(Model):
    admin_level = IntegerField(null=True, blank=True)
    aliases = ManyToManyField('Alias', through="AliasPlace", related_name="place_from_placealias+")
    area_sqkm = IntegerField(null=True, blank=True)
    district_num = IntegerField(null=True, blank=True)
    fips = IntegerField(null=True, blank=True)
    geonameid = IntegerField(null=True, blank=True)
    mls = MultiLineStringField(null=True, blank=True)
    mpoly = MultiPolygonField(null=True, blank=True)
    name = CharField(max_length=200, null=True, blank=True)
    note = CharField(max_length=200, null=True, blank=True)
    objects = GeoManager()
    point = PointField(null=True, blank=True)
    pop = IntegerField(null=True, blank=True)
    pcode = CharField(max_length=200, null=True, blank=True)
    skeleton = MultiLineStringField(null=True, blank=True)
    timezone = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        try:
            return self.name.encode("utf-8")
        except:
            return self.id
    class Meta:
        ordering = ['name']

class ParentChild(Model):
    parent = ForeignKey('Place', related_name="parentplace")
    child = ForeignKey('Place', related_name="subplace")

    #makes sure we can't repeat parent child in db
    class Meta:
        unique_together = (("parent","child"))

class TeamMember(Model):
    email = EmailField(null=True, blank=True)
    name = CharField(max_length=200, null=True, blank=True)
    pic = ImageField(upload_to="images/topicareas", null=True, blank=True)
    position = CharField(max_length=200, null=True, blank=True)
    twitter = CharField(max_length=200, null=True, blank=True)

class Translator(Model):
    name = CharField(max_length=200, null=True, blank=True)


# can also use topics to cirumscribe locations via topic area


#should also probably add in website at some point, so can associate websites with certain topics, too

#also add in feature classes of geonames, so don't mean lake when mean city!