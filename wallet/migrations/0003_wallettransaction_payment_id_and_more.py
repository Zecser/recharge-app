# Generated by Django 5.2.4 on 2025-07-27 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_usermargin_admin_alter_usermargin_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransaction',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='status',
            field=models.CharField(default='success', max_length=20),
        ),
    ]
