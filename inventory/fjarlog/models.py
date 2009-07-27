from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class Budget(models.Model):
        name = models.CharField(max_length=200)

        def __unicode__(self):
                return self.name

class BudgetCategory(models.Model):
        budget = models.ForeignKey(Budget)
        code = models.CharField(max_length=10)
        name = models.CharField(max_length=200)
        parent = models.ForeignKey('BudgetCategory', blank=True, null=True)

        def __unicode__(self):
                return self.name

class BudgetItem(models.Model):
        code = models.CharField(max_length=10)
        name = models.CharField(max_length=200)
        parent = models.ForeignKey(BudgetCategory)
        funds = models.FloatField()

        def __unicode__(self):
                return self.name

class Suggestion(models.Model):
        user = models.ForeignKey(User)
        item = models.ForeignKey(BudgetItem)
        funds = models.FloatField()

        def __unicode__(self):
                return self.user + " : " + self.item

class Comment(models.Model):
        user = models.ForeignKey(User)
        item = models.ForeignKey(BudgetItem)
        date = models.DateTimeField(auto_now=True)
        comment =models.TextField()
        attachment = models.FileField(upload_to="uploaded/%Y/%m/%d/")

        def __unicode__(self):
                return self.user +  " : " + self.item + " @ " + self.date

admin.site.register(Budget)
admin.site.register(BudgetCategory)
admin.site.register(BudgetItem)
admin.site.register(Suggestion)
admin.site.register(Comment)
