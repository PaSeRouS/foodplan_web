from django.db import migrations

def set_allergies(apps, schema_editor):
    SubscriptionType = apps.get_model('web', 'SubscriptionType')

    SubscriptionType.objects.create(
        name='Однодневная',
        duration=1,
        price=99
    )

    SubscriptionType.objects.create(
        name='Недельная',
        duration=7,
        price=199
    )

    SubscriptionType.objects.create(
        name='Месячная',
        duration=30,
        price=399
    )

    SubscriptionType.objects.create(
        name='Квартальная',
        duration=90,
        price=599
    )

    SubscriptionType.objects.create(
        name='Полугодовая',
        duration=180,
        price=799
    )

    SubscriptionType.objects.create(
        name='Годовая',
        duration=365,
        price=999
    )

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_set_allergies'),
    ]

    operations = [
        migrations.RunPython(set_allergies)
    ]