#-*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.gis.db.models import *
from pytz import utc
from shutil import rmtree

class Alert(Model):
    colors = (("danger", "danger"),("info", "info"),("success", "success"),("warning","warning"))
    color = CharField(choices=colors, max_length=200)
    permanent = BooleanField()
    text = CharField(max_length=200)
    user = OneToOneField(User, blank=True, null=True)
    def __str__(self):
        return self.text

#class Account(Model):
#    max_orders = IntegerField() # the maximum number of order this account can make per month
    

    

class AlternateName(Model):
    geonameid = IntegerField(db_index=True)
    isolanguage = CharField(max_length=7, null=True, blank=True)
    alternate_name = CharField(max_length=200, null=True, blank=True, db_index=True)
    isPreferredName = CharField(max_length=1, null=True, blank=True)
    isShortName = CharField(max_length=1, null=True, blank=True)
    isColloquial = CharField(max_length=1, null=True, blank=True)
    isHistoric = CharField(max_length=1, null=True, blank=True)

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
    alias = CharField(max_length=200, null=True, blank=True, db_index=True, unique=True)
    language = CharField(max_length=7, null=True, blank=True, db_index=True)
    class Meta:
        ordering = ['alias']
    def __str__(self):
        return self.alias.encode("utf-8")
    def update(self, d):
        for k,v in d.iteritems():
            setattr(self,k,v)
        self.save()

class AliasPlace(Model):
    alias = ForeignKey('Alias')
    place = ForeignKey('Place')

    class Meta:
        unique_together = (("alias","place"))


class Email(Model):
    address = EmailField(null=True, blank=True)
    entered = DateTimeField(auto_now_add=True)

class Order(Model):
    complete = BooleanField(default=False)
    duration = IntegerField(null=True) # how long it took to process the order
    end = DateTimeField(null=True)
    start = DateTimeField(auto_now_add=True, null=True) # it will never be null, but have to do this because migration asks for default otherwise
    token = CharField(max_length=200, null=True, unique=True) # the random string that's used to find the order in the maps

    def __str__(self):
        return self.token

    def d(self):
        self.delete_map()
        self.delete()

    def delete_map(self):
        rmtree("/home/usrfd/maps/" + self.token)

    def finish(self):
        self.complete = True
        self.end = end = datetime.now().replace(tzinfo=utc)
        self.duration = (end - self.start).total_seconds()
        self.save()

    def update(self, d):
        for k,v in d.iteritems():
            setattr(self,k,v)
        self.save()

# should add in org and person model at some point, so can cross locate story based on people or orgs if no location names given

class Place(Model):
    admin_level = IntegerField(null=True, blank=True, db_index=True)
    admin1_code = CharField(max_length=100, null=True, blank=True, db_index=True)
    admin2_code = CharField(max_length=100, null=True, blank=True, db_index=True)
    aliases = ManyToManyField('Alias', through="AliasPlace", related_name="place_from_placealias+")
    area_sqkm = IntegerField(null=True, blank=True)
    country_code = CharField(max_length=10, null=True, blank=True, db_index=True)
    district_num = IntegerField(null=True, blank=True)
    fips = IntegerField(null=True, blank=True, db_index=True)
    geonameid = IntegerField(null=True, blank=True, db_index=True)
    mls = MultiLineStringField(null=True, blank=True)
    mpoly = MultiPolygonField(null=True, blank=True)
    name = CharField(max_length=200, null=True, blank=True, db_index=True)
    note = CharField(max_length=200, null=True, blank=True)
    objects = GeoManager()
    point = PointField(null=True, blank=True)
    population = BigIntegerField(null=True, blank=True)
    pcode = CharField(max_length=200, null=True, blank=True, db_index=True)
    skeleton = MultiLineStringField(null=True, blank=True)
    timezone = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        try:
            return self.name.encode("utf-8")
        except:
            return self.id
    class Meta:
        ordering = ['name']
    def update(self, d):
        for k,v in d.iteritems():
            setattr(self,k,v)
        self.save()

class ParentChild(Model):
    parent = ForeignKey('Place', related_name="parentplace")
    child = ForeignKey('Place', related_name="subplace")

    #makes sure we can't repeat parent child in db
    class Meta:
        unique_together = (("parent","child"))

# or should I name it attribution??
#class Source(Model):
#    name = CharField(max_length=200)
#    url

class TeamMember(Model):
    email = EmailField(null=True, blank=True)
    name = CharField(max_length=200, null=True, blank=True)
    pic = ImageField(upload_to="images/topicareas", null=True, blank=True)
    position = CharField(max_length=200, null=True, blank=True)
    twitter = CharField(max_length=200, null=True, blank=True)

class Translator(Model):
    name = CharField(max_length=200, null=True, blank=True)

#class UserOrder(Model):
#    user = ForeignKey(User)
#    order = ForeignKey("Order", unique)

#    def __str__(self):
#        return self.user + ":" + self.order


# can also use topics to cirumscribe locations via topic area


#should also probably add in website at some point, so can associate websites with certain topics, too

#also add in feature classes of geonames, so don't mean lake when mean city!
