# Generated by Django 4.2.7 on 2023-11-26 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0005_scamreport'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScamReport',
        ),
    ]