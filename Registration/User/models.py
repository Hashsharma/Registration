from operator import mod
from django.db import models
import datetime
from django.utils import timezone


class UserRegistrationModel(models.Model):
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
    user_first_name = models.CharField(max_length=50, null=True)
    user_last_name = models.CharField(max_length=50, null=True)
    user_email = models.CharField(max_length=50, null=True)
    user_mobile = models.CharField(max_length=10, null=True)
    user_gender = models.IntegerField(null=True)
    user_dob = models.DateField(null=True)
    user_calculated_dob = models.DateField(null=True)
    user_address = models.TextField(null=True)
    user_password = models.TextField(null=True)
    user_created_datetime = models.DateTimeField(null=True)
    user_mod_datetime = models.DateTimeField(null=True)
    user_otp = models.IntegerField(null=True)
    user_active = models.IntegerField(default=1)
    user_ip_address = models.CharField(max_length=50)
    user_type = models.IntegerField(default=2)
    user_product_rid = models.IntegerField(null=False)
    user_mobile_verified = models.SmallIntegerField(default=0)
    user_email_verified = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'users'


class Master(models.Model):
    master_rid = models.AutoField(primary_key=True)
    master_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'master'

