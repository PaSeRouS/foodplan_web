from django.db import migrations

def update_subscriptiontypes(apps, schema_editor):
    SubscriptionType = apps.get_model('web', 'SubscriptionType')

    SubscriptionType.objects.all().delete()

    SubscriptionType.objects.create(
        name='Классическое меню',
        duration=3,
        price=99
    )

    SubscriptionType.objects.create(
        name='Классическое меню',
        duration=6,
        price=79
    )

    SubscriptionType.objects.create(
        name='Классическое меню',
        duration=12,
        price=59
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное меню',
        duration=3,
        price=120
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное меню',
        duration=6,
        price=90
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное меню',
        duration=12,
        price=75
    )

    SubscriptionType.objects.create(
        name='Вегетарианское меню',
        duration=3,
        price=150
    )

    SubscriptionType.objects.create(
        name='Вегетарианское меню',
        duration=6,
        price=120
    )

    SubscriptionType.objects.create(
        name='Вегетарианское меню',
        duration=12,
        price=100
    )

    SubscriptionType.objects.create(
        name='Меню Кето',
        duration=3,
        price=200
    )

    SubscriptionType.objects.create(
        name='Меню Кето',
        duration=6,
        price=150
    )

    SubscriptionType.objects.create(
        name='Меню Кето',
        duration=12,
        price=120
    )

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_subscriptiontype_duration_and_more'),
    ]

    operations = [
        migrations.RunPython(update_subscriptiontypes)
    ]