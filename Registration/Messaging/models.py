from django.db import models

# Create your models here.

class MessageModel(models.Model):

   msg_rid = models.AutoField(primary_key=True)
   msg_number = models.CharField(max_length=10, null=False)
   msg_generated_datetime = models.DateTimeField(null=False)
   msg_status = models.SmallIntegerField(default=0)
   msg_product_rid = models.SmallIntegerField(null=False)
   msg_count = models.SmallIntegerField(null=False)

   class Meta:
       db_table = 'mobile_message'

