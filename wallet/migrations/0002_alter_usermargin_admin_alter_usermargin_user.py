# Generated by Django 4.1.13 on 2025-07-08 01:55

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermargin',
            name='admin',
            field=models.ForeignKey(limit_choices_to={'user_type': accounts.models.UserType['ADMIN']}, on_delete=django.db.models.deletion.CASCADE, related_name='managed_margins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermargin',
            name='user',
            field=models.OneToOneField(limit_choices_to={'user_type__in': [accounts.models.UserType['DISTRIBUTOR'], accounts.models.UserType['RETAILER']]}, on_delete=django.db.models.deletion.CASCADE, related_name='margin_settings', to=settings.AUTH_USER_MODEL),
        ),
    ]
