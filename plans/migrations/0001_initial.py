# Generated by Django 5.2.4 on 2025-07-04 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('validity', models.IntegerField(help_text='Validity in days')),
                ('is_active', models.BooleanField(default=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('identifier', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='plans.provider')),
            ],
            options={
                'verbose_name_plural': 'Plans',
                'ordering': ['created_at'],
            },
        ),
    ]
