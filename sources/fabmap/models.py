from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from django import forms
from django.forms import ModelForm

#
#	Defining models
#
#

class AccessModel(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()

	def __unicode__(self):
		return self.name

class EquipmentCapability(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class EquipmentType(models.Model):
	name = models.CharField(max_length=200)
	maker = models.CharField(max_length=200)
	website = models.URLField(blank=True)
	capabilities = models.ManyToManyField(EquipmentCapability)

	def __unicode__(self):
		return self.maker + " " + self.name

class Site(models.Model):
	lat = models.FloatField("Latitude")
	lon = models.FloatField("Longitude")
	name = models.CharField("Site name", max_length=200)
	locname = models.CharField("Town/city", max_length=200)
	website = models.URLField(blank=True)
	manager = models.ForeignKey(User)
	access = models.ForeignKey(AccessModel, verbose_name="Access model")

	def __unicode__(self):
		return self.name

class Equipment(models.Model):
	type = models.ForeignKey(EquipmentType)
	site = models.ForeignKey(Site)
	notes = models.TextField()

	def __unicode__(self):
		return self.type

#
#	Registering tables with admin site
#
#

admin.site.register(EquipmentType)
admin.site.register(Site)
admin.site.register(EquipmentCapability)
admin.site.register(Equipment)
admin.site.register(AccessModel)


#
#	Defining forms
#
#

class SiteForm(ModelForm):
	class Meta:
		model = Site
		exclude = ('manager')
