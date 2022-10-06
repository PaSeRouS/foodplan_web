from django.db import migrations

def set_allergies(apps, schema_editor):
    Allergy = apps.get_model('web', 'Allergy')

    Allergy.objects.create(
        name='Рыба и морепродукты'
    )

    Allergy.objects.create(
        name='Мясо'
    )

    Allergy.objects.create(
        name='Зерновые'
    )

    Allergy.objects.create(
        name='Продукты пчеловодства'
    )

    Allergy.objects.create(
        name='Орехи и бобовые'
    )

    Allergy.objects.create(
        name='Молочные продукты'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_allergies)
    ]