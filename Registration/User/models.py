from operator import mod
from django.db import models


class Users(models.Model):
    # user_rid = fields.IntField(primary_key=True)
    # user_first_name = fields.StringField(max_length=50)
    # user_last_name = fields.StringField(max_length=50)
    # user_email = fields.StringField(max_length=50, null=False)
    # user_mobile = fields.StringField(max_length=10, null=True)
    # user_gender = fields.IntField(null=False)
    # user_dob = fields.DateField(null=False)
    # user_calculated_dob = fields.DateField()
    # user_address = fields.StringField(null=False)
    # user_password = fields.StringField(null=False)
    # user_created_datetime = fields.DateTimeField()
    # user_mod_datetime = fields.DateTimeField(auto_now=True)
    # user_otp = fields.IntField(null=False)
    # user_active = fields.IntField(default=1)
    # user_ip_address = fields.StringField(max_length=50)
    # user_type = fields.IntField(default=2)
    # user_entity_rid = fields.IntField(max_length=4)

    user_rid = models.AutoField(primary_key=True)
    user_first_name = models.CharField(max_length=50)
    user_last_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50, null=False)
    user_mobile = models.CharField(max_length=10, null=True)
    user_gender = models.IntegerField(null=False)
    user_dob = models.DateField(null=False)
    user_calculated_dob = models.DateField()
    user_address = models.TextField(null=False)
    user_password = models.TextField(null=False)
    user_created_datetime = models.DateTimeField()
    user_mod_datetime = models.DateTimeField(auto_now=True)
    user_otp = models.IntegerField(null=False)
    user_active = models.IntegerField(default=1)
    user_ip_address = models.CharField(max_length=50)
    user_type = models.IntegerField(default=2)
    user_entity_rid = models.IntegerField(null=False)

    class Meta:
        db_table = 'users'


class Master(models.Model):
    master_rid = models.AutoField(primary_key=True)
    master_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'master'

