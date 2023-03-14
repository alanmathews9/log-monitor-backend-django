# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class log(models.Model):
    timestamp = models.DateTimeField()
    application_name = models.CharField(max_length=20)
    level = models.CharField(max_length=10, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    handled_by = models.CharField(max_length=50, blank=True, null=True)
    handled_time = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'


class user(models.Model):
    id = models.IntegerField
    email = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    hashed_password = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'user'



