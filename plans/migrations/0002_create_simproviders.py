from django.db import migrations

def create_providers(apps, schema_editor):
    Provider = apps.get_model('plans', 'Provider')
    Provider.objects.create(title='Airtel')
    Provider.objects.create(title='Jio')
    Provider.objects.create(title='VI')
    Provider.objects.create(title='BSNL')

class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_providers),
    ]
