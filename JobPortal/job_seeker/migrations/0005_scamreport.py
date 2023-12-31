# Generated by Django 4.2.7 on 2023-11-26 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruiter', '0007_rename_company_name_and_details_jobpost_company'),
        ('job_seeker', '0004_delete_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScamReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('scam_recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruiter.jobpost')),
            ],
        ),
    ]
