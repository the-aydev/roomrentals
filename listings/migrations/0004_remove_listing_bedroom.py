# Generated by Django 3.2.7 on 2021-10-27 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_listing_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bedroom',
        ),
    ]