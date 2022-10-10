from django.db import migrations

def update_subscriptiontypes(apps, schema_editor):
    SubscriptionType = apps.get_model('web', 'SubscriptionType')
    Subscription = apps.get_model('web', 'Subscription')

    Subscription.objects.all().delete()
    SubscriptionType.objects.all().delete()

    SubscriptionType.objects.create(
        name='Классическое',
        duration=3,
        price=99,
        description='Все блюда в данной подборке направлены на получения удовольствия от процесса употребления пищи.'
    )

    SubscriptionType.objects.create(
        name='Классическое',
        duration=6,
        price=79,
        description='Все блюда в данной подборке направлены на получения удовольствия от процесса употребления пищи.'
    )

    SubscriptionType.objects.create(
        name='Классическое',
        duration=12,
        price=59,
        description='Все блюда в данной подборке направлены на получения удовольствия от процесса употребления пищи.'
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное',
        duration=3,
        price=120,
        description='Меню, в котором количество углеводов в блюдах значительно сокращено.'
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное',
        duration=6,
        price=90,
        description='Меню, в котором количество углеводов в блюдах значительно сокращено.'
    )

    SubscriptionType.objects.create(
        name='Низкоуглеводное',
        duration=12,
        price=75,
        description='Меню, в котором количество углеводов в блюдах значительно сокращено.'
    )

    SubscriptionType.objects.create(
        name='Вегетарианское',
        duration=3,
        price=150,
        description='Вегетарианское меню сордержит в себе блюда из продуктов растительного происхождения, главным образом из зерновых продуктов, овощей, фруктов, орехов. Полностью исключается мясо животных, птицы, рыбы.'
    )

    SubscriptionType.objects.create(
        name='Вегетарианское',
        duration=6,
        price=120,
        description='Вегетарианское меню сордержит в себе блюда из продуктов растительного происхождения, главным образом из зерновых продуктов, овощей, фруктов, орехов. Полностью исключается мясо животных, птицы, рыбы.'
    )

    SubscriptionType.objects.create(
        name='Вегетарианское',
        duration=12,
        price=100,
        description='Вегетарианское меню сордержит в себе блюда из продуктов растительного происхождения, главным образом из зерновых продуктов, овощей, фруктов, орехов. Полностью исключается мясо животных, птицы, рыбы.'
    )

    SubscriptionType.objects.create(
        name='Кето',
        duration=3,
        price=200,
        description='Меню с блюдами, в которых основной акцент направлен на жиры и белки.'
    )

    SubscriptionType.objects.create(
        name='Кето',
        duration=6,
        price=150,
        description='Меню с блюдами, в которых основной акцент направлен на жиры и белки.'
    )

    SubscriptionType.objects.create(
        name='Кето',
        duration=12,
        price=120,
        description='Меню с блюдами, в которых основной акцент направлен на жиры и белки.'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_subscriptiontype_description'),
    ]

    operations = [
        migrations.RunPython(update_subscriptiontypes)
    ]