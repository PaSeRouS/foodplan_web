from django.db import migrations

def update_subscriptiontypes(apps, schema_editor):
    SubscriptionType = apps.get_model('web', 'SubscriptionType')
    Subscription = apps.get_model('web', 'Subscription')

    Subscription.objects.all().delete()
    SubscriptionType.objects.all().delete()

    SubscriptionType.objects.create(
        name='Классическое',
        duration=3,
        price=99
    )

    SubscriptionType.objects.create(
        name='Классическое',
        duration=6,
        price=79
    )

    SubscriptionType.objects.create(
        name='Классическое',
        duration=12,
        price=59
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное',
        duration=3,
        price=120
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное',
        duration=6,
        price=90
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное',
        duration=12,
        price=75
    )

    SubscriptionType.objects.create(
        name='Вегетарианское',
        duration=3,
        price=150
    )

    SubscriptionType.objects.create(
        name='Вегетарианское',
        duration=6,
        price=120
    )

    SubscriptionType.objects.create(
        name='Вегетарианское',
        duration=12,
        price=100
    )

    SubscriptionType.objects.create(
        name='Кето',
        duration=3,
        price=200
    )

    SubscriptionType.objects.create(
        name='Кето',
        duration=6,
        price=150
    )

    SubscriptionType.objects.create(
        name='Кето',
        duration=12,
        price=120
    )

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_rename_unit_title_ingredientquantity_unit_label'),
    ]

    operations = [
        migrations.RunPython(update_subscriptiontypes)
    ]