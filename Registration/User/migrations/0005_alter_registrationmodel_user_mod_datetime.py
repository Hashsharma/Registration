# Generated by Django 4.1.2 on 2022-10-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_alter_registrationmodel_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationmodel',
            name='user_mod_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
