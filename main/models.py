# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.CharField(max_length=30, blank=True, null=True)
    user_pass = models.CharField(max_length=30, blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    #test = models.TextField(max_length=255, blank=True, null=True)
    #test2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'users'


class CreatreTasks(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    id_users = models.IntegerField(blank=True, null=True)
    inputtitle = models.CharField(max_length=30, blank=True, null=True)
    textarea = models.TextField(max_length=300, blank=True, null=True)


    class Meta:
        #managed = True
        db_table = 'createtask'