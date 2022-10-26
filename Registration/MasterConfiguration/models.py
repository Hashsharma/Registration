from django.db import models

# Create your models here
from django.db import models

class MasterConfigurationModels(models.Model):

    config_rid = models.AutoField(primary_key=True)
    config_code = models.CharField(max_length=50, null=False)
    config_name = models.CharField(max_length=255, null=False)
    config_url = models.CharField(max_length=255, null=True)
    config_description = models.CharField(max_length=255, null=True)
    config_valid = models.SmallIntegerField(null=False)
    config_product_rid = models.IntegerField(null=False)
    config_created_datetime = models.DateTimeField(null=False)
    config_code_mod_datetime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'configuration'